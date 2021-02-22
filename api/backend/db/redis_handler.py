import redis
from loguru import logger
from omegaconf import OmegaConf

from models import EvalSample, EvalResult


class RedisHandler(object):
    _singleton = None
    __samples: redis.Redis = None
    __results: redis.Redis = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            logger.info('Instantiating RedisHandler!')
            cls._singleton = super(RedisHandler, cls).__new__(cls)

            # setup redis
            conf = OmegaConf.load('config/config.yml')
            r_host = conf.backend.redis.host
            r_port = conf.backend.redis.port

            r_sample_db_idx = conf.backend.redis.sample_db_idx
            cls.__samples = redis.Redis(host=r_host, port=r_port, db=r_sample_db_idx)
            assert cls.__samples.ping(), f"Couldn't connect to Redis DB {r_sample_db_idx} at {r_host}:{r_port}!"

            r_result_db_idx = conf.backend.redis.result_db_idx
            cls.__results = redis.Redis(host=r_host, port=r_port, db=r_result_db_idx)
            assert cls.__results.ping(), f"Couldn't connect to Redis DB {r_result_db_idx} at {r_host}:{r_port}!"

        return cls._singleton

    def __close(self) -> None:
        logger.info('Shutting down RedisHandler!')
        self.__samples.close()
        self.__results.close()

    def store_sample(self, sample: EvalSample) -> str:
        if self.__samples.set(sample.id, sample.json()) != 1:
            logger.error(f"Cannot store EvalSample {sample.id}")
        logger.info(f"Successfully stored EvalSample {sample.id}")
        return sample.id

    def load_sample(self, sample_id: str) -> EvalSample:
        s = self.__samples.get(sample_id)
        if s is None:
            logger.error(f"Cannot load EvalSample {sample_id}")
        else:
            sample = EvalSample.parse_raw(s)
            logger.info(f"Successfully loaded EvalSample {sample.id}")
            return sample

    def sample_exists(self, sample_id: str) -> bool:
        return bool(self.__samples.exists(sample_id))

    def random_sample(self):
        rand_id = self.__samples.randomkey()
        return self.load_sample(sample_id=rand_id)

    def store_result(self, result: EvalResult) -> str:
        if self.__results.set(result.id, result.json()) != 1:
            logger.error(f"Cannot store EvalResult {result.id}")
        logger.info(f"Successfully stored EvalResult {result.id}")
        return result.id

    def load_result(self, result_id: str) -> EvalResult:
        s = self.__results.get(result_id)
        if s is None:
            logger.error(f"Cannot load EvalResult {result_id}")
        else:
            result = EvalResult.parse_raw(s)
            logger.info(f"Successfully loaded EvalResult {result.id}")
            return result
