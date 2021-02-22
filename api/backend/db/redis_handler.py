import redis
from loguru import logger
from omegaconf import OmegaConf


class RedisHandler(object):
    _singleton = None
    __client: redis.Redis = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            logger.info('Instantiating RedisHandler!')
            cls._singleton = super(RedisHandler, cls).__new__(cls)

            # setup redis
            conf = OmegaConf.load('config/config.yml')
            r_host = conf.backend.redis.host
            r_port = conf.backend.redis.port
            r_db_idx = conf.backend.redis.db_idx

            cls.__client = redis.Redis(host=r_host, port=r_port, db=r_db_idx)
            assert cls.__client.ping(), f"Couldn't connect to Redis DB {r_db_idx} at {r_host}:{r_port}!"

        return cls._singleton
