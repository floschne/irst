from typing import List

from pydantic import Field, root_validator

import models
from models import StudyType
from .base_result import BaseResult


class RatingResult(BaseResult):
    ratings: List[float] = Field(description="Ratings of the Images of the related RatingSample")

    @root_validator
    def rating_for_every_image_must_exist(cls, values):
        if models.__validation_disabled__:
            return values

        sample_id = values.get('sample_id')
        ratings = values.get('ratings')
        if sample_id is None or ratings is None:
            raise ValueError(f"sample_id and ratings must not be None!")

        from backend.db import RedisHandler
        rs = RedisHandler().load_rating_sample(rs_id=sample_id.strip())
        if len(ratings) != len(rs.image_ids):
            raise ValueError(f"Number of ratings and number of images of the RatingSample do not match!")
        return values

    @root_validator
    def ratings_must_be_in_min_max_interval(cls, values):
        if models.__validation_disabled__:
            return values

        sample_id = values.get('sample_id')
        ratings = values.get('ratings')
        if sample_id is None or ratings is None:
            raise ValueError(f"sample_id and ratings must not be None!")

        from backend.db import RedisHandler
        rs = RedisHandler().load_rating_sample(rs_id=sample_id.strip())
        if min(ratings) < rs.min_rating or max(ratings) > rs.max_rating:
            raise ValueError(f"Ratings must be in min max interval of the related RatingSample!")
        return values

    @staticmethod
    def get_type() -> StudyType:
        return StudyType.RATING
