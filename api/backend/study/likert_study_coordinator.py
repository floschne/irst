from loguru import logger

from backend.db import RedisHandler
from backend.study import StudyCoordinatorBase
from config import conf
from models import ModelRanking
from models import LikertSample


class LikertStudyCoordinator(StudyCoordinatorBase):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = super(LikertStudyCoordinator, cls).__new__(cls)
        return cls.__singleton

    def __init__(self):
        # hack to only init the StudyCoordinatorBase if not already done (since THIS is a singleton)
        if getattr(self, 'num_top_k_imgs', None) is None:
            sub_conf = conf.study_initialization.likert_samples
            super().__init__("likert",
                             sub_conf.num_top_k_imgs,
                             sub_conf.num_samples,
                             sub_conf.in_prog_ttl)
            self.question = sub_conf.question
            self.answers = list(sub_conf.answers)
            self.answer_weights = list(sub_conf.answer_weights)

            if not len(self.answers) == len(self.answer_weights):
                logger.error("The number of answers and weights does not match!")
                raise ValueError("The number of answers and weights does not match!")

            # we need this for whatever pythonic reason (it's not accessible from self.__rh from the super class)
            self.__rh = RedisHandler()

    def _generate_sample(self, mr: ModelRanking) -> LikertSample:
        # get top-k from model ranking
        tk_imgs = mr.top_k_image_ids[0:self.num_top_k_imgs]

        # create the sample
        ls = LikertSample(mr_id=mr.id,
                          caption=mr.query,
                          image_ids=tk_imgs[:self.num_top_k_imgs],
                          question=self.question,
                          answers=self.answers,
                          answer_weights=self.answer_weights)
        # and persist in redis
        self.__rh.store_likert_sample(ls)

        return ls
