import threading
from typing import Optional, List

import redis
from loguru import logger
from omegaconf import OmegaConf

from models import EvalSample, EvalResult, GroundTruthSample


class RedisHandler(object):
    __singleton = None
    __sync_lock = None
    __eval_samples: redis.Redis = None
    __gt_samples: redis.Redis = None
    __results: redis.Redis = None

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
            assert cls.__eval_samples.ping(), f"Couldn't connect to Redis DB {r_eval_sample_db_idx} at {r_host}:{r_port}!"

            r_gt_sample_db_idx = conf.backend.redis.gt_sample_db_idx
            cls.__gt_samples = redis.Redis(host=r_host, port=r_port, db=r_gt_sample_db_idx)
            assert cls.__gt_samples.ping(), f"Couldn't connect to Redis DB {r_gt_sample_db_idx} at {r_host}:{r_port}!"

            r_progress_db_idx = conf.backend.redis.progress_db_idx
            cls.__progress = redis.Redis(host=r_host, port=r_port, db=r_progress_db_idx)
            assert cls.__progress.ping(), f"Couldn't connect to Redis DB {r_progress_db_idx} at {r_host}:{r_port}!"

            r_result_db_idx = conf.backend.redis.result_db_idx
            cls.__results = redis.Redis(host=r_host, port=r_port, db=r_result_db_idx)
            assert cls.__results.ping(), f"Couldn't connect to Redis DB {r_result_db_idx} at {r_host}:{r_port}!"

        return cls.__singleton

    def get_progress_client(self):
        return self.__progress

    def __close(self) -> None:
        logger.info("Shutting down RedisHandler!")
        self.__eval_samples.close()
        self.__gt_samples.close()
        self.__results.close()
        self.__progress.close()

    def flush_all(self):
        logger.warning(f"Flushing Redis DBs!")
        self.__eval_samples.flushdb()
        self.__gt_samples.flushdb()
        self.__results.flushdb()
        self.__progress.flushdb()

    # TODO: I know there is a lot of redundant code here, which could be simplified by inheritance, flags AND TIME...

    ################# Images #################

    def store_image_ids(self, gts: GroundTruthSample):
        # store in progress DB because in __gt_samples we need KEYS to get all GTS...
        self.__progress.sadd('gt_images', *gts.top_k_image_ids)

    def get_random_image_ids(self, num: int = 1) -> List[str]:
        # store in progress DB because in __gt_samples we need KEYS to get all GTS...
        return self.__progress.srandmember('gt_images', num)

    ################# GroundTruthSample #################

    def store_gt_sample(self, gts: GroundTruthSample) -> str:
        if self.__gt_samples.set(gts.id, gts.json()) != 1:
            logger.error(f"Cannot store GroundTruthSample {gts.id}")

        # store all associated image ids
        self.store_image_ids(gts)

        logger.debug(f"Successfully stored GroundTruthSample {gts.id}")
        return gts.id

    def load_gt_sample(self, gts_id: str) -> GroundTruthSample:
        s = self.__gt_samples.get(gts_id)
        if s is None:
            logger.error(f"Cannot load GroundTruthSample {gts_id}")
        else:
            sample = GroundTruthSample.parse_raw(s)
            logger.debug(f"Successfully loaded GroundTruthSample {sample.id}")
            return sample

    def gt_sample_exists(self, gts_id: str) -> bool:
        return bool(self.__gt_samples.exists(gts_id))

    def get_all_gts_ids(self) -> List[str]:
        return self.__gt_samples.keys()

    ################# EvalSample #################

    def store_eval_sample(self, sample: EvalSample) -> str:
        if self.__eval_samples.set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store EvalSample {sample.id}")
        logger.debug(f"Successfully stored EvalSample {sample.id}")
        return sample.id

    def load_eval_sample(self, sample_id: str) -> Optional[EvalSample]:
        s = self.__eval_samples.get(sample_id)
        if s is None:
            logger.error(f"Cannot load EvalSample {sample_id}")
            return None
        else:
            sample = EvalSample.parse_raw(s)
            logger.debug(f"Successfully loaded EvalSample {sample.id}")
            return sample

    def eval_sample_exists(self, sample_id: str) -> bool:
        return bool(self.__eval_samples.exists(sample_id))

    ################# EvalResult #################

    def store_result(self, result: EvalResult) -> Optional[str]:
        if not self.eval_sample_exists(result.es_id):
            logger.error(
                f"EvalSample {result.es_id} referenced in EvalResult {result.id} does not exist! Discarding!")
            return None

        if not self.__results.set(result.id, result.json()) != 1:
            logger.error(f"Cannot store EvalResult {result.id}")
            return None
        else:
            logger.debug(f"Successfully stored EvalResult {result.id}")
            return result.id

    def load_result(self, result_id: str) -> EvalResult:
        s = self.__results.get(result_id)
        if s is None:
            logger.error(f"Cannot load EvalResult {result_id}")
        else:
            result = EvalResult.parse_raw(s)
            logger.debug(f"Successfully loaded EvalResult {result.id}")
            return result
