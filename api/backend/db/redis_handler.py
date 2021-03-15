import pprint
import json
import threading
from typing import Optional, List, Dict

import redis
from loguru import logger
from omegaconf import OmegaConf

from models import EvalSample, EvalResult, ModelRanking


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
            conf = OmegaConf.load('config/config.yml')
            r_host = conf.backend.redis.host
            r_port = conf.backend.redis.port

            r_eval_sample_db_idx = conf.backend.redis.eval_sample_db_idx
            cls.__eval_samples = redis.Redis(host=r_host, port=r_port, db=r_eval_sample_db_idx)
            assert cls.__eval_samples.ping(), f"Couldn't connect to Redis EVAL SAMPLE DB {r_eval_sample_db_idx} at {r_host}:{r_port}!"

            r_m_rank_db_idx = conf.backend.redis.m_rank_db_idx
            cls.__m_rankings = redis.Redis(host=r_host, port=r_port, db=r_m_rank_db_idx)
            assert cls.__m_rankings.ping(), f"Couldn't connect to Redis MODEL RANKING DB {r_m_rank_db_idx} at {r_host}:{r_port}!"

            r_progress_db_idx = conf.backend.redis.progress_db_idx
            cls.__progress = redis.Redis(host=r_host, port=r_port, db=r_progress_db_idx)
            assert cls.__progress.ping(), f"Couldn't connect to Redis PROGRESS DB {r_progress_db_idx} at {r_host}:{r_port}!"

            r_result_db_idx = conf.backend.redis.result_db_idx
            cls.__results = redis.Redis(host=r_host, port=r_port, db=r_result_db_idx)
            assert cls.__results.ping(), f"Couldn't connect to Redis RESULT DB {r_result_db_idx} at {r_host}:{r_port}!"

            r_auth_db_idx = conf.backend.redis.auth_db_idx
            cls.__auth = redis.Redis(host=r_host, port=r_port, db=r_auth_db_idx)
            assert cls.__auth.ping(), f"Couldn't connect to Redis AUTH DB {r_auth_db_idx} at {r_host}:{r_port}!"

            r_mturk_db_idx = conf.backend.redis.mturk_db_idx
            cls.__mturk = redis.Redis(host=r_host, port=r_port, db=r_mturk_db_idx)
            assert cls.__mturk.ping(), f"Couldn't connect to Redis MTURK DB {r_mturk_db_idx} at {r_host}:{r_port}!"

        return cls.__singleton

    def get_progress_client(self):
        return self.__progress

    def get_auth_client(self):
        return self.__auth

    def shutdown(self) -> None:
        logger.info("Shutting down RedisHandler!")
        self.__progress.close()
        self.__eval_samples.close()
        self.__m_rankings.close()
        self.__results.close()
        self.__auth.close()
        self.__mturk.close()

    def flush(self, auth: bool = False, mturk: bool = False):
        logger.warning(f"Flushing Redis DBs!")
        self.__eval_samples.flushdb()
        self.__m_rankings.flushdb()
        self.__results.flushdb()
        self.__progress.flushdb()
        if auth:
            self.__auth.flushdb()
        if mturk:
            self.__mturk.flushdb()
        # save necessary when deployed via docker
        self.__eval_samples.save()
        self.__m_rankings.save()
        self.__results.save()
        self.__progress.save()
        if auth:
            self.__auth.save()
        if mturk:
            self.__mturk.save()

    # TODO: I know there is a lot of redundant code here, which could be simplified by inheritance, flags AND TIME...

    ################# Images #################

    def store_image_ids(self, mr: ModelRanking):
        # store in progress DB because in __m_rankings we need KEYS to get all MRs...
        self.__progress.sadd('m_rankings', *mr.top_k_image_ids)

    def get_random_image_ids(self, num: int = 1) -> List[str]:
        # store in progress DB because in __m_rankings we need KEYS to get all MRs...
        return self.__progress.srandmember('m_rankings', num)

    ################# ModelRanking #################

    def store_model_ranking(self, mr: ModelRanking) -> str:
        if self.__m_rankings.set(mr.id, mr.json()) != 1:
            logger.error(f"Cannot store ModelRanking {mr.json()}")

        # store all associated image ids
        self.store_image_ids(mr)

        logger.debug(f"Successfully stored ModelRanking {mr.id}")
        return mr.id

    def load_model_ranking(self, mr_id: str) -> Optional[ModelRanking]:
        s = self.__m_rankings.get(mr_id)
        if s is None:
            logger.error(f"Cannot load ModelRanking {mr_id}")
            return None
        else:
            sample = ModelRanking.parse_raw(s)
            logger.debug(f"Successfully loaded ModelRanking {sample.id}")
            return sample

    def model_ranking_exists(self, mr_id: str) -> bool:
        return bool(self.__m_rankings.exists(mr_id))

    def get_all_mr_ids(self) -> List[str]:
        return self.__m_rankings.keys()

    ################# EvalSample #################

    def store_eval_sample(self, sample: EvalSample) -> str:
        if self.__eval_samples.set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store EvalSample {sample.json()}")
        logger.debug(f"Successfully stored EvalSample {sample.id}")
        return sample.id

    def load_eval_sample(self, sample_id: str, verbose: bool = True) -> Optional[EvalSample]:
        s = self.__eval_samples.get(sample_id)
        if s is None:
            logger.error(f"Cannot load EvalSample {sample_id}")
            return None
        else:
            sample = EvalSample.parse_raw(s)
            if verbose:
                logger.debug(f"Successfully loaded EvalSample {sample.id}")
            return sample

    def eval_sample_exists(self, sample_id: str) -> bool:
        return bool(self.__eval_samples.exists(sample_id))

    def list_eval_samples(self) -> List[EvalSample]:
        es = [self.load_eval_sample(sample_id=es_id, verbose=False) for es_id in self.__eval_samples.keys()]
        logger.debug(f"Retrieved {len(es)} EvalSamples!")
        return es

    ################# EvalResult #################

    def store_result(self, result: EvalResult) -> Optional[str]:
        if not self.eval_sample_exists(result.es_id):
            logger.error(
                f"EvalSample {result.es_id} referenced in EvalResult {result.id} does not exist! Discarding!")
            return None

        if self.__results.set(result.id, result.json()) != 1:
            logger.error(f"Cannot store EvalResult {result.json()}")
            return None
        else:
            logger.debug(f"Successfully stored EvalResult {result.id}")
            return result.id

    def load_result(self, result_id: str) -> Optional[EvalResult]:
        s = self.__results.get(result_id)
        if s is None:
            logger.error(f"Cannot load EvalResult {result_id}")
            return None
        else:
            result = EvalResult.parse_raw(s)
            logger.debug(f"Successfully loaded EvalResult {result.id}")
            return result

    ############### MTURK ##############################

    def store_hit_info(self, hit_info: Dict, es: EvalSample) -> Optional[str]:
        # we cannot use json.dumps(hit_info) because it throws an error since datetime objects are not json serializable
        if self.__mturk.set(str(es.id + '_hit_info').encode('utf-8'), pprint.pformat(hit_info)) != 1:
            logger.error(f"Cannot store  HIT Info {hit_info['HIT']['HITId']} for EvalSample {es.id}")
            return None

        logger.debug(f"Successfully stored HIT Info {hit_info['HIT']['HITId']} for EvalSample {es.id}")
        return es.id

    def load_hit_info(self, es: EvalSample) -> Optional[Dict]:
        s = self.__mturk.get(str(es.id + '_hit_info').encode('utf-8'))
        if s is None:
            logger.error(f"Cannot retrieve HIT Info for EvalSample {es.id}")
            return None
        else:
            logger.debug(f"Successfully loaded HIT Info for EvalSample {es.id}")
            return json.loads(s)

    def list_hit_ids(self):
        ids = self.__mturk.keys('*_hit_info')
        logger.debug(f"Found {len(ids)} HIT IDs")
