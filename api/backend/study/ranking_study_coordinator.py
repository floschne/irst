import numpy as np

from backend.db import RedisHandler
from backend.study import StudyCoordinatorBase
from config import conf
from models import RankingSample, ModelRanking


class RankingStudyCoordinator(StudyCoordinatorBase):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = super(RankingStudyCoordinator, cls).__new__(cls)
        return cls.__singleton

    def __init__(self):
        # hack to only init the StudyCoordinatorBase if not already done (since THIS is a singleton)
        if getattr(self, 'num_top_k_imgs', None) is None:
            sub_conf = conf.study_initialization.ranking_samples
            super().__init__("ranking",
                             sub_conf.num_top_k_imgs,
                             sub_conf.num_samples,
                             sub_conf.in_prog_ttl)
            self.num_random_imgs = sub_conf.num_random_imgs
            # we need this for whatever pythonic reason (it's not accessible from self.__rh from the super class)
            self.__rh = RedisHandler()

    def _generate_sample(self, mr: ModelRanking) -> RankingSample:
        # get top-k from model ranking
        tk_imgs = mr.top_k_image_ids[0:self.num_top_k_imgs]
        # get  random images
        random_imgs = set(self.__rh.get_random_image_ids(self.num_random_imgs))

        # make sure intersection of the top-k and the random images is an empty set!
        mr_top_k_imgs = set(mr.top_k_image_ids)  # order doesnt matter for checking
        while len(mr_top_k_imgs.intersection(random_imgs)) != 0:
            # sample new random images if there was an overlap
            random_imgs = set(self.__rh.get_random_image_ids(self.num_random_imgs))

        # combine random images and top-k images
        es_imgs = tk_imgs + list(random_imgs)

        # shuffle so users cannot observe patterns so easy
        np.random.shuffle(es_imgs)

        # create the sample
        rs = RankingSample(mr_id=mr.id,
                           query=mr.query,
                           image_ids=es_imgs)
        # and store in redis
        self.__rh.store_ranking_sample(rs)

        return rs
