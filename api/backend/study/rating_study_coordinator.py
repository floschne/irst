from loguru import logger

from backend.db import RedisHandler
from backend.study import StudyCoordinatorBase
from config import conf
from models import ModelRanking, RatingSample, StudyType


class RatingStudyCoordinator(StudyCoordinatorBase):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = super(RatingStudyCoordinator, cls).__new__(cls)
        return cls.__singleton

    def __init__(self):
        # hack to only init the StudyCoordinatorBase if not already done (since THIS is a singleton)
        if getattr(self, 'num_top_k_imgs', None) is None:
            sub_conf = conf.study_initialization[StudyType.RATING]
            super().__init__(StudyType.RATING,
                             sub_conf.num_top_k_imgs,
                             sub_conf.num_samples,
                             sub_conf.in_prog_ttl)
            self.min_rating = sub_conf.min_rating
            self.max_rating = sub_conf.max_rating
            self.rating_step = sub_conf.rating_step

            if self.min_rating > self.max_rating:
                logger.error("Minimum rating has to be smaller than maximum rating!")
                raise ValueError("Minimum rating has to be smaller than maximum rating!")

    def _generate_sample(self, mr: ModelRanking) -> RatingSample:
        # get top-k from model ranking
        tk_imgs = mr.top_k_image_ids[0:self.num_top_k_imgs]

        # create the sample
        rs = RatingSample(mr_id=mr.id,
                          caption=mr.query,
                          image_ids=tk_imgs[:self.num_top_k_imgs],
                          min_rating=self.min_rating,
                          max_rating=self.max_rating,
                          rating_step=self.rating_step)
        # and persist in redis
        RedisHandler().store_rating_sample(rs)

        return rs
