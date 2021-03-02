import concurrent
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum, unique
from typing import Dict, Union, List

import redis
from loguru import logger
from omegaconf import OmegaConf

from backend import ImageServer
from backend.db import RedisHandler
from init_redis_data import init_redis_data
from models import EvalResult, EvalSample


@unique
class Keys(bytes, Enum):
    TODO = b"todo"
    IN_PROGRESS = b"in_progress"
    DONE = b"done"
    RUN_CNT = b"run_cnt"
    RUN_RESULTS = b"run_results_"
    TTL = b"__ttl_shadow__"


def expired_handler():
    rh = RedisHandler()
    progress = rh.get_progress_client()
    while True:
        try:
            # if a es_id is in in_progress but not in KEYS, the es_id is expired.
            # we have to be careful here with bytes and strings! every key is handled as bytes and combining with str
            # leads to hard-to-find errors...
            in_prog_ids = set(progress.smembers(Keys.IN_PROGRESS))
            ttk_shadow_keys = list(progress.keys(Keys.TTL.value + b"*"))
            ttl_shadow_ids = set([key.replace(Keys.TTL.value, b"") for key in ttk_shadow_keys])
            expired = list(in_prog_ids - ttl_shadow_ids)
            StudyCoordinator().expire(expired)
            time.sleep(0.1)
        except Exception as e:
            print(e)


class StudyCoordinator(object):
    __singleton = None
    __sync_lock: threading.Lock = None
    __rh: RedisHandler = None
    __is: ImageServer = None
    __progress: redis.Redis = None
    __num_top_k_imgs: int = None
    __num_random_k_imgs: int = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info('Instantiating StudyCoordinator!')
            cls.__singleton = super(StudyCoordinator, cls).__new__(cls)

            cls.__is = ImageServer()

            # lock object for critical sections
            cls.__sync_lock = threading.Lock()

            # get redis client
            cls.__rh = RedisHandler()
            cls.__progress = cls.__rh.get_progress_client()

            conf = OmegaConf.load('config/config.yml')
            cls.__num_top_k_imgs = conf.study.samples.num_top_k_imgs
            cls.__num_random_k_imgs = conf.study.samples.num_random_k_imgs
            cls.__in_prog_ttl = conf.study.samples.in_prog_ttl
            cls.__init_data_root = conf.study.init.data_root
            cls.__init_flush = conf.study.init.flush
            cls.__init_num_samples = conf.study.init.num_samples

            # setup expired watcher
            cls.expired_watcher = ThreadPoolExecutor(max_workers=1)
            cls.expired_watcher.submit(expired_handler)

        return cls.__singleton

    # noinspection PyUnresolvedReferences,PyProtectedMember
    def shutdown(self):
        logger.info('Shutting down StudyCoordinator!')
        # clear remaining futures
        # https://gist.github.com/clchiou/f2608cbe54403edb0b13
        self.expired_watcher._threads.clear()
        concurrent.futures.thread._threads_queues.clear()
        self.expired_watcher.shutdown(wait=False)

    def init_study(self):
        # initialize Redis data
        logger.info("Initializing Redis data")
        init_redis_data(data_root=self.__init_data_root,
                        flush=self.__init_flush,
                        num_samples=self.__init_num_samples)
        # init run count with 0
        self.__set_run_count(0)
        logger.info(f"Successfully initialized Study")

        self.__start_new_run()

    def __start_new_run(self):
        self.__init_todo()
        self.__init_done()
        self.__init_in_progress()
        self.__set_run_count(int(self.__current_run()) + 1)

        logger.info(f"Successfully started Study Run {self.__current_run()}")
        logger.info(f"Current Progress: {self.current_progress()}")

    def __init_todo(self):
        # init todo set (initially contains all GTSample IDs)
        gts_ids = self.__rh.get_all_gts_ids()
        if len(gts_ids) == 0:
            logger.error("Redis not initialized!")
            raise RuntimeError("Redis not initialized!")

        self.__progress.delete(Keys.TODO)

        # generate an EvalSample for each GTS
        eval_samples = [self.__generate_eval_sample(gts_id) for gts_id in gts_ids]
        # add their reverences (IDs) to todo
        self.__progress.sadd(Keys.TODO, *[es.id for es in eval_samples])

        if self.__progress.scard(Keys.TODO) != len(eval_samples):
            logger.error("Error while initializing ToDo List!")
            raise RuntimeError("Error while initializing ToDo List!")

        logger.info(f"Successfully initialized {Keys.TODO} List!")
        logger.info(f"Current Progress: {self.current_progress()}")

    def __generate_eval_sample(self, gts_id: str) -> EvalSample:
        gts = self.__rh.load_gt_sample(gts_id)
        tk_imgs = set(gts.top_k_image_ids[0:self.__num_top_k_imgs])
        random_imgs = set(self.__rh.get_random_image_ids(self.__num_random_k_imgs))

        # make sure intersection set has 0 elements!
        while len(tk_imgs & random_imgs) != 0:
            random_imgs = set(self.__rh.get_random_image_ids(self.__num_random_k_imgs))

        es = EvalSample(gts_id=gts.id,
                        query=gts.query,
                        image_ids=list(tk_imgs.union(random_imgs)))
        self.__rh.store_eval_sample(es)

        return es

    def __init_done(self):
        # init done set (empty set)
        self.__progress.delete(Keys.DONE)
        logger.info(f"Successfully initialized {Keys.DONE} List!")

    def __init_in_progress(self):
        # remove all in-progress ids
        in_prog_ids = self.__progress.keys(f"{Keys.IN_PROGRESS}*")
        if len(in_prog_ids) > 0:
            self.__progress.delete(*in_prog_ids)
        logger.info(f"Successfully initialized {Keys.IN_PROGRESS} List!")

    def next(self) -> Union[EvalSample, int]:
        with self.__sync_lock:
            # get random ES (id) from todo list
            es_id = self.__progress.srandmember(Keys.TODO)
            if es_id is None:
                # the todo list is empty so we return the shortest TTL of the in_progess ist
                return self.__shortest_ttl()

            # move to in_progress list
            self.__progress.smove(Keys.TODO, Keys.IN_PROGRESS, es_id)
            logger.info(f"Moved EvalSample {es_id} from TODO to IN_PROGRESS!")
            logger.info(f"Current Progress: {self.current_progress()}")
            # create shadow element with TTL
            self.__progress.set(Keys.TTL.value + es_id, "ttl_proxy", ex=self.__in_prog_ttl)
            # load and return the actual ES per ID
            return self.__rh.load_eval_sample(es_id)

    def __shortest_ttl(self) -> int:
        in_prog_es_ids = self.__progress.smembers(Keys.IN_PROGRESS)
        ttls = sorted([self.__progress.ttl(Keys.TTL.value + es_id) for es_id in in_prog_es_ids])
        return ttls[-1]

    def expire(self, es_ids: List[str]):
        with self.__sync_lock:
            # move the from in_progress back to todo
            for es_id in es_ids:
                self.__progress.smove(Keys.IN_PROGRESS, Keys.TODO, es_id)
                logger.info(f"EvalSample {es_id} expired in IN_PROGRESS and moved back to TODO!")
                logger.info(f"Current Progress: {self.current_progress()}")

    def submit(self, res: EvalResult):
        with self.__sync_lock:
            logger.info(f"EvalResult {res.id} submission received!")
            # store the EvalResult
            self.__rh.store_result(res)
            # reference the EvalResult in the current run results
            self.__reference_in_current_run_results(res)
            # move referenced EvalSample to DONE
            self.__progress.smove(Keys.IN_PROGRESS, Keys.DONE, res.es_id)
            logger.info(f"Moved EvalSample {res.es_id} from IN_PROGRESS to DONE")
            prog = self.current_progress()
            logger.info(f"Current Progress: {prog}")

            # if this was the last remaining EvalSample, we start a new study run
            if self.__study_run_finished():
                self.__start_new_run()

    def __reference_in_current_run_results(self, res: EvalResult):
        self.__progress.sadd(self.__current_run_results_key(), res.id)
        logger.info(f"Successfully referenced EvalResult {res.id} in results of current run {self.__current_run()}!")

    def __reset_previous_results(self):
        # reset all run results
        current_run = self.__progress.get(Keys.RUN_CNT)
        if current_run is not None:
            while current_run >= 0:
                self.__progress.delete(self.__run_results_key(current_run))
        logger.info(f"Successfully reset all results from previous Study runs!")

    def __set_run_count(self, run_cnt: int = 1):
        with self.__sync_lock:
            self.__progress.set(Keys.RUN_CNT, run_cnt)

    def __current_run_results_key(self) -> str:
        return self.__run_results_key(self.__current_run())

    def __run_results_key(self, run_cnt: int) -> str:
        return f"{Keys.RUN_RESULTS}{run_cnt}"

    def __num_todo(self) -> int:
        return self.__progress.scard(Keys.TODO)

    def __num_done(self) -> int:
        return self.__progress.scard(Keys.DONE)

    def __num_in_progress(self) -> int:
        return self.__progress.scard(Keys.IN_PROGRESS)

    def __current_run(self) -> int:
        return self.__progress.get(Keys.RUN_CNT)

    def current_progress(self) -> Dict[str, int]:
        return {
            'num_todo': self.__num_todo(),
            'num_in_progress': self.__num_in_progress(),
            'num_done': self.__num_done(),
            'num_total': len(self.__rh.get_all_gts_ids()),
            'run': self.__current_run()
        }

    def __study_run_finished(self) -> bool:
        prog = self.current_progress()
        if prog['num_todo'] == ['num_in_progress'] == 0 and prog['num_done'] == prog['num_total']:
            return True
        elif (prog['num_todo'] == ['num_in_progress'] == 0 and prog['num_done'] != prog['num_total']) or \
                (prog['num_todo'] == ['num_in_progress'] != 0 and prog['num_done'] == prog['num_total']):
            logger.error("Erroneous state of study progress!")
            logger.error(f"Current Progress: {prog}")
        else:
            return False
