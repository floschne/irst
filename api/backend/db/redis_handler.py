import json
import pprint
import threading
from typing import Optional, List, Dict, Union

import redis
from loguru import logger

from config import conf
from models import RankingSample, RankingResult, ModelRanking, Feedback, LikertSample, LikertResult, StudyType, \
    BaseSample, BaseResult, RatingResult, RatingSample, RatingWithFocusSample, RatingWithFocusResult


class RedisHandler(object):
    __singleton = None
    __sync_lock = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info('Instantiating RedisHandler!')
            cls.__singleton = super(RedisHandler, cls).__new__(cls)

            # lock object for critical sections
            cls.__sync_lock = threading.Lock()

            # setup redis
            r_host = conf.backend.redis.host
            r_port = conf.backend.redis.port

            # setup clients
            cls.__clients = {}
            for client, db_idx in conf.backend.redis.clients.items():
                cls.__clients[client.lower()] = redis.Redis(host=r_host, port=r_port, db=db_idx)
                assert cls.__clients[client].ping(), \
                    f"Couldn't connect to Redis {str(client).upper()} DB #{db_idx} at {r_host}:{r_port}!"
                logger.info(f"Successfully connected to Redis {str(client).upper()} DB #{db_idx}")

        return cls.__singleton

    def get_progress_client(self, typ: str):
        return self.__clients[f'{typ.lower()}_progress']

    def get_auth_client(self):
        return self.__clients['auth']

    @logger.catch(reraise=True)
    def shutdown(self) -> None:
        logger.info("Shutting down RedisHandler!")
        for client in self.__clients.values():
            client.close()

    @logger.catch(reraise=True)
    def flush(self, auth: bool = False, mturk: bool = False):
        which = 'STUDY DATA'
        if auth and mturk:
            which = 'ALL'
        elif auth:
            which += ' AND AUTH'
        elif mturk:
            which += ' AND MTURK'

        logger.warning(f"Flushing {which} Redis DBs!")
        for client_name, client in self.__clients.items():
            if not auth and client_name == 'auth':
                continue
            elif not mturk and client_name == 'mturk':
                continue
            else:
                client.flushdb()
                client.save()

    # TODO: I know there is a lot of redundant code here, which could be simplified by inheritance, flags AND TIME...

    ################# Images #################

    @logger.catch(reraise=True)
    def store_image_ids(self, mr: ModelRanking):
        # store in progress DB because in __m_rankings we need KEYS to get all MRs...
        self.__clients['images'].sadd('m_rankings', *mr.top_k_image_ids)

    @logger.catch(reraise=True)
    def get_random_image_ids(self, num: int = 1) -> List[str]:
        # store in progress DB because in __m_rankings we need KEYS to get all MRs...
        return [str(i, encoding='utf-8') for i in self.__clients['images'].srandmember('m_rankings', num)]

    ################# ModelRanking #################

    @logger.catch(reraise=True)
    def store_model_ranking(self, mr: ModelRanking) -> str:
        if self.__clients['model_ranking'].set(mr.id, mr.json()) != 1:
            logger.error(f"Cannot store ModelRanking {mr.json()}")

        # store all associated image ids
        self.store_image_ids(mr)

        logger.debug(f"Successfully stored ModelRanking {mr.id}")
        return mr.id

    @logger.catch(reraise=True)
    def load_model_ranking(self, mr_id: str, verbose=False) -> Optional[ModelRanking]:
        s = self.__clients['model_ranking'].get(mr_id)
        if s is None:
            logger.error(f"Cannot load ModelRanking {mr_id}")
            return None
        else:
            sample = ModelRanking.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded ModelRanking {sample.id}")
            return sample

    @logger.catch(reraise=True)
    def model_ranking_exists(self, mr_id: str) -> bool:
        return bool(self.__clients['model_ranking'].exists(mr_id))

    @logger.catch(reraise=True)
    def list_all_model_ranking_ids(self) -> List[str]:
        return self.__clients['model_ranking'].keys()

    @logger.catch(reraise=True)
    def list_model_rankings(self, num: int = None) -> List[ModelRanking]:
        mrs = [self.load_model_ranking(mr_id=mr_id, verbose=False) for mr_id in self.list_all_model_ranking_ids()[:num]]
        logger.debug(f"Found {len(mrs)} ModelRankings!")
        return mrs

    ################# RankingSample #################

    @logger.catch(reraise=True)
    def store_ranking_sample(self, sample: RankingSample) -> str:
        if self.__clients['ranking_sample'].set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store RankingSample {sample.json()}")
        logger.debug(f"Successfully stored RankingSample {sample.id}")
        return sample.id

    @logger.catch(reraise=True)
    def load_ranking_sample(self, rs_id: str, verbose: bool = True) -> Optional[RankingSample]:
        s = self.__clients['ranking_sample'].get(rs_id)
        if s is None:
            logger.error(f"Cannot load RankingSample {rs_id}")
            return None
        else:
            sample = RankingSample.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RankingSample {sample.id}")
            return sample

    @logger.catch(reraise=True)
    def ranking_sample_exists(self, rs_id: str) -> bool:
        return bool(self.__clients['ranking_sample'].exists(rs_id))

    @logger.catch(reraise=True)
    def list_ranking_samples(self, num: Optional[int] = None) -> List[RankingSample]:
        rs = [self.load_ranking_sample(rs_id=rs_id, verbose=False) for rs_id in
              self.__clients['ranking_sample'].keys()[:num]]
        logger.debug(f"Found {len(rs)} RankingSamples!")
        return rs

    ################# RankingResult #################

    @logger.catch(reraise=True)
    def store_ranking_result(self, result: RankingResult) -> Optional[str]:
        if not self.ranking_sample_exists(result.sample_id):
            logger.error(
                f"RankingSample {result.sample_id} referenced in RankingResult {result.id} does not exist! Discarding!")
            return None

        if self.__clients['ranking_result'].set(result.id, result.json()) != 1:
            logger.error(f"Cannot store RankingResult {result.json()}")
            return None
        else:
            logger.debug(f"Successfully stored RankingResult {result.id}")
            return result.id

    @logger.catch(reraise=True)
    def load_ranking_result(self, rr_id: str, verbose: bool = False) -> Optional[RankingResult]:
        s = self.__clients['ranking_result'].get(rr_id)
        if s is None:
            logger.error(f"Cannot load RankingResult {rr_id}")
            return None
        else:
            result = RankingResult.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RankingResult {result.id}")
            return result

    @logger.catch(reraise=True)
    def list_ranking_results(self) -> List[RankingResult]:
        res = [self.load_ranking_result(rr_id=res_id, verbose=False) for res_id in
               self.__clients['ranking_result'].keys()]
        logger.debug(f"Found {len(res)} RankingResults!")
        return res

    ################# LikertSample #################

    @logger.catch(reraise=True)
    def store_likert_sample(self, sample: LikertSample) -> str:
        if self.__clients['likert_sample'].set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store LikertSample {sample.json()}")
        logger.debug(f"Successfully stored LikertSample {sample.id}")
        return sample.id

    @logger.catch(reraise=True)
    def load_likert_sample(self, ls_id: str, verbose: bool = True) -> Optional[LikertSample]:
        s = self.__clients['likert_sample'].get(ls_id)
        if s is None:
            logger.error(f"Cannot load LikertSample {ls_id}")
            return None
        else:
            sample = LikertSample.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded LikertSample {sample.id}")
            return sample

    @logger.catch(reraise=True)
    def likert_sample_exists(self, ls_id: str) -> bool:
        return bool(self.__clients['likert_sample'].exists(ls_id))

    @logger.catch(reraise=True)
    def list_likert_samples(self, num: Optional[int] = None) -> List[LikertSample]:
        ls = [self.load_likert_sample(ls_id=ls_id, verbose=False) for ls_id in
              self.__clients['likert_sample'].keys()[:num]]
        logger.debug(f"Found {len(ls)} LikertSamples!")
        return ls

    ################# LikertResult #################

    @logger.catch(reraise=True)
    def store_likert_result(self, result: LikertResult) -> Optional[str]:
        if not self.likert_sample_exists(result.sample_id):
            logger.error(
                f"LikertSample {result.sample_id} referenced in LikertResult {result.id} does not exist! Discarding!")
            return None

        if self.__clients['likert_result'].set(result.id, result.json()) != 1:
            logger.error(f"Cannot store LikertResult {result.json()}")
            return None
        else:
            logger.debug(f"Successfully stored LikertResult {result.id}")
            return result.id

    @logger.catch(reraise=True)
    def load_likert_result(self, lr_id: str, verbose: bool = False) -> Optional[LikertResult]:
        s = self.__clients['likert_result'].get(lr_id)
        if s is None:
            logger.error(f"Cannot load LikertResult {lr_id}")
            return None
        else:
            result = LikertResult.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded LikertResult {result.id}")
            return result

    @logger.catch(reraise=True)
    def list_likert_results(self) -> List[LikertResult]:
        res = [self.load_likert_result(lr_id=res_id, verbose=False) for res_id in
               self.__clients['likert_result'].keys()]
        logger.debug(f"Found {len(res)} LikertResults!")
        return res

    ################# RatingSample #################

    @logger.catch(reraise=True)
    def store_rating_sample(self, sample: RatingSample) -> str:
        if self.__clients['rating_sample'].set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store RatingSample {sample.json()}")
        logger.debug(f"Successfully stored RatingSample {sample.id}")
        return sample.id

    @logger.catch(reraise=True)
    def load_rating_sample(self, rs_id: str, verbose: bool = True) -> Optional[RatingSample]:
        s = self.__clients['rating_sample'].get(rs_id)
        if s is None:
            logger.error(f"Cannot load RatingSample {rs_id}")
            return None
        else:
            sample = RatingSample.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RatingSample {sample.id}")
            return sample

    @logger.catch(reraise=True)
    def rating_sample_exists(self, rs_id: str) -> bool:
        return bool(self.__clients['rating_sample'].exists(rs_id))

    @logger.catch(reraise=True)
    def list_rating_samples(self, num: Optional[int] = None) -> List[RatingSample]:
        ls = [self.load_rating_sample(rs_id=rs_id, verbose=False) for rs_id in
              self.__clients['rating_sample'].keys()[:num]]
        logger.debug(f"Found {len(ls)} RatingSamples!")
        return ls

    ################# RatingResult #################

    @logger.catch(reraise=True)
    def store_rating_result(self, result: RatingResult) -> Optional[str]:
        if not self.rating_sample_exists(result.sample_id):
            logger.error(
                f"RatingSample {result.sample_id} referenced in RatingResult {result.id} does not exist! Discarding!")
            return None

        if self.__clients['rating_result'].set(result.id, result.json()) != 1:
            logger.error(f"Cannot store RatingResult {result.json()}")
            return None
        else:
            logger.debug(f"Successfully stored RatingResult {result.id}")
            return result.id

    @logger.catch(reraise=True)
    def load_rating_result(self, rr_id: str, verbose: bool = False) -> Optional[RatingResult]:
        s = self.__clients['rating_result'].get(rr_id)
        if s is None:
            logger.error(f"Cannot load RatingResult {rr_id}")
            return None
        else:
            result = RatingResult.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RatingResult {result.id}")
            return result

    @logger.catch(reraise=True)
    def list_rating_results(self) -> List[RatingResult]:
        res = [self.load_rating_result(rr_id=res_id, verbose=False) for res_id in
               self.__clients['rating_result'].keys()]
        logger.debug(f"Found {len(res)} RatingResults!")
        return res

    ################# RatingWithFocusSample #################

    @logger.catch(reraise=True)
    def store_rating_with_focus_sample(self, sample: RatingWithFocusSample) -> str:
        if self.__clients['rating_with_focus_sample'].set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store RatingWithFocusSample {sample.json()}")
        logger.debug(f"Successfully stored RatingWithFocusSample {sample.id}")
        return sample.id

    @logger.catch(reraise=True)
    def load_rating_with_focus_sample(self, rs_id: str, verbose: bool = True) -> Optional[RatingWithFocusSample]:
        s = self.__clients['rating_with_focus_sample'].get(rs_id)
        if s is None:
            logger.error(f"Cannot load RatingWithFocusSample {rs_id}")
            return None
        else:
            sample = RatingWithFocusSample.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RatingWithFocusSample {sample.id}")
            return sample

    @logger.catch(reraise=True)
    def rating_with_focus_sample_exists(self, rs_id: str) -> bool:
        return bool(self.__clients['rating_with_focus_sample'].exists(rs_id))

    @logger.catch(reraise=True)
    def list_rating_with_focus_samples(self, num: Optional[int] = None) -> List[RatingWithFocusSample]:
        ls = [self.load_rating_with_focus_sample(rs_id=rs_id, verbose=False) for rs_id in
              self.__clients['rating_with_focus_sample'].keys()[:num]]
        logger.debug(f"Found {len(ls)} RatingWithFocusSample!")
        return ls

    ################# RatingResult #################

    @logger.catch(reraise=True)
    def store_rating_with_focus_result(self, result: RatingWithFocusResult) -> Optional[str]:
        if not self.rating_with_focus_sample_exists(result.sample_id):
            logger.error((f"RatingWithFocusSample {result.sample_id} referenced in RatingWithFocusResult {result.id}"
                          " does not exist! Discarding!"))
            return None

        if self.__clients['rating_with_focus_result'].set(result.id, result.json()) != 1:
            logger.error(f"Cannot store RatingWithFocusResult {result.json()}")
            return None
        else:
            logger.debug(f"Successfully stored RatingWithFocusResult {result.id}")
            return result.id

    @logger.catch(reraise=True)
    def load_rating_with_focus_result(self, rr_id: str, verbose: bool = False) -> Optional[RatingWithFocusResult]:
        s = self.__clients['rating_with_focus_result'].get(rr_id)
        if s is None:
            logger.error(f"Cannot load RatingResult {rr_id}")
            return None
        else:
            result = RatingWithFocusResult.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded RatingResult {result.id}")
            return result

    @logger.catch(reraise=True)
    def list_rating_with_focus_results(self) -> List[RatingWithFocusResult]:
        res = [self.load_rating_with_focus_result(rr_id=res_id, verbose=False) for res_id in
               self.__clients['rating_with_focus_result'].keys()]
        logger.debug(f"Found {len(res)} RatingWithFocusResult!")
        return res

    ############### MTURK ##############################

    @logger.catch(reraise=True)
    def store_hit_info(self, hit_info: Dict, sample: BaseSample) -> Optional[str]:
        # we cannot use json.dumps(hit_info) because it throws an error since datetime objects are not json serializable
        if self.__clients['mturk'].set(str(sample.id + '_hit_info').encode('utf-8'),
                                       pprint.pformat(hit_info).encode('utf-8')) != 1:
            logger.error(
                f"Cannot store Info of HIT {hit_info['HITId']} for {sample.get_type().capitalize()}Sample {sample.id}")
            return None

        logger.debug(
            f"Successfully stored HIT Info {hit_info['HITId']} for {sample.get_type().capitalize()}Sample {sample.id}")
        return sample.id

    @logger.catch(reraise=True)
    def load_hit_info(self, sample: BaseSample) -> Optional[Dict]:
        s = self.__clients['mturk'].get(str(sample.id + '_hit_info').encode('utf-8'))
        if s is None:
            logger.error(f"Cannot retrieve HIT Info for {sample.get_type().capitalize()}Sample {sample.id}")
            return None
        else:
            logger.debug(f"Successfully loaded HIT Info for {sample.get_type().capitalize()}Sample {sample.id}")
            return json.loads(s)

    @logger.catch(reraise=True)
    def list_hit_ids(self) -> List[str]:
        keys = self.__clients['mturk'].keys('*_hit_info')
        return [json.loads(self.__clients['mturk'].get(key))['HITId'] for key in keys]

    ############### FEEDBACK (in MTurk DB) ##############################

    @logger.catch(reraise=True)
    def store_feedback(self, feedback: Feedback) -> Optional[str]:
        # store
        key = str('feedback_' + feedback.id)
        if self.__clients['mturk'].set(key.encode('utf-8'), feedback.json()) != 1:
            logger.error(f"Cannot store Feedback {feedback.id} for RankingSample {feedback.sample_id}")
            return None

        # reference in sample set
        set_key = str(feedback.sample_id + '_feedback')
        if self.__clients['mturk'].sadd(set_key.encode('utf-8'), feedback.id) != 1:
            logger.error(f"Cannot reference Feedback {feedback.id} with Sample {feedback.sample_id}")
            return None
        else:
            logger.debug(f"Successfully referenced Feedback {feedback.id} with Sample {feedback.sample_id}")

        logger.debug(f"Successfully stored Feedback {feedback.sample_id} for Sample {feedback.sample_id}")
        return feedback.id

    @logger.catch(reraise=True)
    def load_feedback(self, fb_id: str) -> Optional[Feedback]:
        key = str('feedback_' + fb_id)
        fb = self.__clients['mturk'].get(key.encode('utf-8'))
        if fb is None:
            logger.error(f"Cannot retrieve Feedback {fb_id}")
            return None
        else:
            logger.debug(f"Successfully loaded Feedback {fb_id}")
            return Feedback.parse_raw(fb)

    @logger.catch(reraise=True)
    def list_feedbacks_of_sample(self, sample_id: str) -> List[Feedback]:
        key = str(sample_id + '_feedback')
        return [self.load_feedback(str(fb_id, 'utf-8')) for fb_id in
                self.__clients['mturk'].smembers(key.encode('utf-8'))]

    @logger.catch(reraise=True)
    def list_all_feedbacks(self) -> List[Feedback]:
        fb_ids = []
        for key in self.__clients['mturk'].keys('*_feedback'):
            fb_ids.extend(self.__clients['mturk'].smembers(key))

        return [self.load_feedback(str(fb_id, 'utf-8')) for fb_id in fb_ids]

    ############### LIKERT_SAMPLE AND RANKING_SAMPLE ##############################

    @logger.catch(reraise=True)
    def sample_exists(self, sample_id: str, return_type=False) -> Union[bool, StudyType]:
        if self.ranking_sample_exists(sample_id):
            if return_type:
                return StudyType.RANKING
            return True
        elif self.likert_sample_exists(sample_id):
            if return_type:
                return StudyType.LIKERT
            return True
        elif self.rating_sample_exists(sample_id):
            if return_type:
                return StudyType.RATING
            return True
        elif self.rating_with_focus_sample_exists(sample_id):
            if return_type:
                return StudyType.RATING_WITH_FOCUS
            return True
        else:
            logger.error(("Neither a RankingSample, a RatingSample, a RatingWithFocusSample, nor a LikertSample"
                          f" with ID '{sample_id}' exists!"))
            return False

    @logger.catch(reraise=True)
    def load_sample(self, sample_id: str) -> Optional[BaseSample]:
        if self.ranking_sample_exists(sample_id):
            return self.load_ranking_sample(rs_id=sample_id)
        elif self.likert_sample_exists(sample_id):
            return self.load_likert_sample(ls_id=sample_id)
        elif self.rating_sample_exists(sample_id):
            return self.load_rating_sample(rs_id=sample_id)
        elif self.rating_with_focus_sample_exists(sample_id):
            return self.load_rating_with_focus_sample(rs_id=sample_id)
        else:
            logger.error(("Neither a RankingSample, a RatingSample, a RatingWithFocusSample, nor a LikertSample"
                          f" with ID '{sample_id}' exists!"))
            return None

    @logger.catch(reraise=True)
    def store_result(self, res: BaseResult) -> Optional[str]:
        if isinstance(res, RankingResult):
            return self.store_ranking_result(res)
        elif isinstance(res, LikertResult):
            return self.store_likert_result(res)
        elif isinstance(res, RatingResult):
            return self.store_rating_result(res)
        elif isinstance(res, RatingWithFocusResult):
            return self.store_rating_with_focus_result(res)
        else:
            logger.error("Only RankingResult, LikertResult, RatingResult, and RatingWithFocusResult are supported!")
            raise NotImplementedError(
                "Only RankingResult, LikertResult, RatingResult, and RatingWithFocusResult are supported!")
