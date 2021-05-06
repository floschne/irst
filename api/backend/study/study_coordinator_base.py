from __future__ import annotations

import concurrent
import glob
import os
import threading
import time
from abc import abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum, unique
from typing import Dict, Union, List, Optional

import numpy as np
import pandas as pd
import redis
from loguru import logger

from backend.image_server import ImageServer
from backend.db import RedisHandler
from config import conf
from models import RankingResult, RankingSample, ModelRanking, LikertResult, LikertSample

@unique
class InitState(int, Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


@unique
class Keys(bytes, Enum):
    TODO = b"todo"
    IN_PROGRESS = b"in_progress"
    DONE = b"done"
    INIT_STATE = b"init_lvl"
    RUN_CNT = b"run_cnt"
    RUN_RESULTS = b"run_results_"
    TTL = b"__ttl_shadow__"


def expired_handler(coordinator: StudyCoordinatorBase):
    rh = RedisHandler()
    progress = rh.get_progress_client(coordinator.typ)
    while True:
        try:
            # if a sample id is in in_progress but not in KEYS, the sample id is expired.
            # we have to be careful here with bytes and strings! every key is handled as bytes and combining with str
            # leads to hard-to-find errors...
            in_prog_ids = set(progress.smembers(Keys.IN_PROGRESS))
            ttk_shadow_keys = list(progress.keys(Keys.TTL.value + b"*"))
            ttl_shadow_ids = set([key.replace(Keys.TTL.value, b"") for key in ttk_shadow_keys])
            expired = list(in_prog_ids - ttl_shadow_ids)
            coordinator.expire(expired)
            time.sleep(0.1)
        except Exception as e:
            print(e)


class StudyCoordinatorBase(object):
    __sync_lock: threading.Lock = None
    __rh: RedisHandler = None
    __is: ImageServer = None
    __progress: redis.Redis = None

    def __init__(self, typ: str, num_top_k_imgs: int, num_samples: int, in_prog_ttl: int):
        logger.info(f"Instantiating {typ.capitalize()}Study Coordinator")

        self.typ = typ
        self.num_top_k_imgs = num_top_k_imgs
        self.num_samples = num_samples if num_samples > 1 else None
        self.in_prog_ttl = in_prog_ttl

        self.__is = ImageServer()

        # lock object for critical sections
        self.__sync_lock = threading.Lock()

        # get redis client
        self.__rh = RedisHandler()
        self.__progress = self.__rh.get_progress_client(typ)

        # common config for model rankings
        self.__init_data_root = conf.study_initialization.model_rankings.data_root
        self.__init_flush = conf.study_initialization.model_rankings.flush
        self.__init_shuffle = conf.study_initialization.model_rankings.shuffle

        # setup expired watcher
        self.expired_watcher = ThreadPoolExecutor(max_workers=1)
        self.expired_watcher.submit(expired_handler, coordinator=self)

        # set init state to todo
        self.__progress.set(Keys.INIT_STATE, InitState.TODO.value, nx=True)

    @abstractmethod
    def _generate_sample(self, mr: ModelRanking) -> Union[RankingSample, LikertSample]:
        pass

    def init_study(self):
        # we wait a random amount of time here to support multi-processing (gunicorn spawns multiple processes) so
        # only the instance that reads the init_flag first will init Redis! Otherwise it gets initialized multiple
        # times
        time.sleep(np.random.uniform(low=0.05, high=0.5))
        init_state = self.__progress.get(Keys.INIT_STATE)
        if init_state is not None and int(init_state) == InitState.TODO.value:
            # set init state to in_progress
            self.__progress.set(Keys.INIT_STATE, InitState.IN_PROGRESS.value)

            # initialize model rankings (only if not done before)
            if len(self.__rh.list_all_model_ranking_ids()) == 0:
                self.__init_model_rankings()

            # init run count with 0
            self.__set_run_count(0)
            # set init state to done
            self.__progress.set(Keys.INIT_STATE, InitState.DONE.value)
            logger.info(f"Successfully initialized {self.typ.upper()} Study")

            self.__start_new_run()
        logger.info(f"{self.typ.upper()} Study already started! Current Progress: {self.current_progress()}")

    def __init_model_rankings(self):
        data_root = conf.study_initialization.model_rankings.data_root
        if not os.path.lexists(data_root) or not os.path.isdir(data_root):
            logger.error(f"Cannot read data root {data_root}")
            raise FileNotFoundError(f"Cannot find data root at {data_root}")

        # find the feather serialized Dataframe in the data root
        feathers = glob.glob(os.path.join(data_root, "*.df.feather"))
        if len(feathers) != 1:
            logger.error(
                f"Found multiple Dataframes! Please make sure only one Dataframe like '*.df.feather'"
                f"exists is in {data_root}!"
            )
            raise FileExistsError(
                f"Found multiple Dataframes! Please make sure only one Dataframe like '*.df.feather'"
                f"exists is in {data_root}!"
            )

        logger.info(f"Initializing ModelRankings from Dataframe {feathers[0]}")
        # load the Dataframe
        df = pd.read_feather(feathers[0])

        # make sure the mandatory columns exist
        for k in ['sample_id', 'caption', 'top_k_matches']:
            if k not in df.columns:
                logger.error(f"Cannot find {k} in the columns of the DataFrame!")
                raise IndexError(f"Cannot find {k} in the columns of the DataFrame!")

        # we don't use lambda for cleaner code
        def generate_model_ranking(row) -> ModelRanking:
            return ModelRanking(ds_id=row['sample_id'],
                                query=row['caption'],
                                top_k_image_ids=row['top_k_matches'].tolist())

        # generate ModelRankings from DataFrame
        rankings = df.apply(generate_model_ranking, axis=1).tolist()

        # shuffle and slice
        if conf.study_initialization.model_rankings.shuffle:
            np.random.shuffle(rankings)
        if self.num_samples > 1:
            rankings = rankings[:self.num_samples]

        # store the ModelRankings
        for mr in rankings:
            self.__rh.store_model_ranking(mr)

    def __start_new_run(self):
        self.__init_todo()
        self.__init_done()
        self.__init_in_progress()
        self.__set_run_count(int(self.__current_run()) + 1)

        logger.info(f"Successfully started {self.typ.upper()} Study Run  #{self.__current_run()}")
        logger.info(f"Current {self.typ.upper()} Study Progress: {self.current_progress()}")

    def __init_todo(self):
        # init to do set (initially contains all ModelRanking IDs)
        mr_ids = self.__rh.list_all_model_ranking_ids()
        if len(mr_ids) == 0:
            logger.error("ModelRankings not initialized!")
            raise RuntimeError("ModelRankings not initialized!")

        self.__progress.delete(Keys.TODO)

        # generate num_samples Samples from ModelRankings
        samples = [self._generate_sample(mr) for mr in self.__rh.list_model_rankings(num=self.num_samples)]

        # add their reverences (IDs) to todo
        self.__progress.sadd(Keys.TODO, *[rs.id for rs in samples])

        if self.__progress.scard(Keys.TODO) != len(samples):
            logger.error("Error while initializing ToDo List!")
            raise RuntimeError("Error while initializing ToDo List!")

        logger.info(f"Successfully initialized {Keys.TODO} List!")
        logger.info(f"Current Progress: {self.current_progress()}")

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

    # noinspection PyUnresolvedReferences,PyProtectedMember
    def shutdown(self):
        logger.info(f'Shutting down {self.typ.capitalize()}StudyCoordinator!')
        # clear remaining futures
        # https://gist.github.com/clchiou/f2608cbe54403edb0b13
        self.expired_watcher._threads.clear()
        concurrent.futures.thread._threads_queues.clear()
        self.expired_watcher.shutdown(wait=False)

    def initialization_is_done(self) -> bool:
        init_state = self.__progress.get(Keys.INIT_STATE)
        return init_state is not None and int(init_state) == InitState.DONE.value

    def next(self) -> Union[RankingSample, LikertSample, int]:
        with self.__sync_lock:
            # get random sample (id) from to do list
            sample_id = self.__progress.srandmember(Keys.TODO)
            if sample_id is None:
                # the to do list is empty so we return the shortest TTL of the in_progess ist
                return self.__shortest_ttl()

            # move to in_progress list
            self.__progress.smove(Keys.TODO, Keys.IN_PROGRESS, sample_id)
            logger.info(f"Moved Sample {sample_id} from TODO to IN_PROGRESS!")
            logger.info(f"Current Progress: {self.current_progress()}")
            # create shadow element with TTL
            self.__progress.set(Keys.TTL.value + sample_id, "ttl_proxy", ex=self.in_prog_ttl)
            # load and return the actual sample per ID
            return self.__rh.load_sample(sample_id)

    def __shortest_ttl(self) -> int:
        in_prog_ids = self.__progress.smembers(Keys.IN_PROGRESS)
        ttls = sorted([self.__progress.ttl(Keys.TTL.value + sample_id) for sample_id in in_prog_ids], reverse=True)
        return ttls[0]

    def expire(self, sample_ids: List[str]):
        with self.__sync_lock:
            # move the from in_progress back to todo
            for sample_id in sample_ids:
                self.__progress.smove(Keys.IN_PROGRESS, Keys.TODO, sample_id)
                logger.info(f"Sample {sample_id} expired in IN_PROGRESS and moved back to TODO!")
                logger.info(f"Current Progress: {self.current_progress()}")

    def submit(self, res: Union[RankingResult, LikertResult]) -> Optional[str]:
        # TODO this is not the real OOP way to do this... --> make super class for RankingResult and LikertResult
        with self.__sync_lock:
            # TODO do we want to accept this or raise an exception?!
            if self.typ == 'ranking' and isinstance(res, LikertResult):
                logger.warning(f"Submitting LikertResult to {self.typ.capitalize()}StudyCoordinator")
            if self.typ == 'likert' and isinstance(res, RankingResult):
                logger.warning(f"Submitting RankingResult to {self.typ.capitalize()}StudyCoordinator")
            else:
                logger.error("Only RankingResult and LikertResult are supported!")
                raise NotImplementedError("Only RankingResult and LikertResult are supported!")

            logger.info(f"{self.typ.capitalize()}Result {res.id} submission received!")

            # if the Result is NOT for MTurk, check if the Sample is already expired in in_prog set
            if isinstance(res, RankingResult):
                sample_id = res.rs_id.encode('utf-8')
            else:  # isinstance(res, LikertResult)
                sample_id = res.ls_id.encode('utf-8')

            if res.mt_params is None and sample_id not in self.__progress.smembers(Keys.IN_PROGRESS):
                logger.warning(
                    f"{self.typ.capitalize()}Sample '{sample_id}' referenced by {self.typ.capitalize()}Result"
                    f"'{res.id}' already expired in IN_PROGRESS! Submission Rejected"
                )
                return None

            # store the Result
            if self.__rh.store_result(res) is None:
                return None

            # only coordinate the study if the result is NOT for MTurk
            if res.mt_params is None:
                # reference the Result in the current run results
                self.__reference_in_current_run_results(res)
                # move referenced Sample to DONE
                self.__progress.smove(Keys.IN_PROGRESS, Keys.DONE, sample_id)
                logger.info(f"Moved {self.typ.capitalize()}Sample {sample_id} from IN_PROGRESS to DONE")
                prog = self.current_progress()
                logger.info(f"Current Progress: {prog}")

                # if this was the last remaining RankingSample, we start a new study run
                if self.__study_run_finished():
                    self.__start_new_run()

        return res.id

    def __reference_in_current_run_results(self, res: Union[RankingResult, LikertResult]):
        self.__progress.sadd(self.__current_run_results_key(), res.id)
        logger.info(f"Successfully referenced RankingResult {res.id} in results of current run {self.__current_run()}!")

    # TODO remove this ?!
    # def __reset_previous_results(self):
    #     # reset all run results
    #     current_run = self.__progress.get(Keys.RUN_CNT)
    #     if current_run is not None:
    #         while current_run >= 0:
    #             self.__progress.delete(self.__run_results_key(current_run))
    #     logger.info(f"Successfully reset all results from previous Study runs!")

    def __set_run_count(self, run_cnt: int = 1):
        self.__progress.set(Keys.RUN_CNT, run_cnt)

    def __current_run_results_key(self) -> str:
        return self.__run_results_key(self.__current_run())

    @staticmethod
    def __run_results_key(run_cnt: int) -> str:
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
        n_todo = self.__num_todo()
        n_in_prog = self.__num_in_progress()
        n_done = self.__num_done()
        return {
            'num_todo': n_todo,
            'num_in_progress': n_in_prog,
            'num_done': n_done,
            'num_total': n_todo + n_in_prog + n_done,
            'run': self.__current_run()
        }

    def __study_run_finished(self) -> bool:
        prog = self.current_progress()
        if prog['num_todo'] == prog['num_in_progress'] == 0 and prog['num_done'] == prog['num_total']:
            return True
        elif (prog['num_todo'] == prog['num_in_progress'] == 0 and prog['num_done'] != prog['num_total']) or \
                (prog['num_todo'] == prog['num_in_progress'] != 0 and prog['num_done'] == prog['num_total']):
            logger.error("Erroneous state of study progress!")
            logger.error(f"Current Progress: {prog}")
        else:
            return False
