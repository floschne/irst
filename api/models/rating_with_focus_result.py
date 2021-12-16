from typing import List

from pydantic import Field, root_validator

import models
from models import StudyType
from .base_result import BaseResult


class RatingWithFocusResult(BaseResult):
    context_ratings: List[float] = Field(
        description="Context ratings of the Images of the related RatingWithFocusSample")
    focus_ratings: List[float] = Field(description="Focus ratings of the Images of the related RatingWithFocusSample")

    @root_validator
    def rating_for_every_image_must_exist(cls, values):
        if models.__validation_disabled__:
            return values

        sample_id = values.get('sample_id')
        context_ratings = values.get('context_ratings')
        focus_ratings = values.get('focus_ratings')
        if not (sample_id or context_ratings or focus_ratings):
            raise ValueError(f"sample_id and ratings must not be None!")

        from backend.db import RedisHandler
        rs = RedisHandler().load_rating_with_focus_sample(rs_id=sample_id.strip())
        if len(context_ratings) != len(focus_ratings) or len(focus_ratings) != len(rs.image_ids):
            raise ValueError(f"Number of ratings and number of images of the RatingWithFocusSample do not match!")
        return values

    @root_validator
    def ratings_must_be_in_min_max_interval(cls, values):
        if models.__validation_disabled__:
            return values

        sample_id = values.get('sample_id')
        context_ratings = values.get('context_ratings')
        focus_ratings = values.get('focus_ratings')
        if not (sample_id or context_ratings or focus_ratings):
            raise ValueError(f"sample_id and ratings must not be None!")

        from backend.db import RedisHandler
        rs = RedisHandler().load_rating_with_focus_sample(rs_id=sample_id.strip())
        if min(context_ratings) < rs.min_rating or max(context_ratings) > rs.max_rating or \
                min(focus_ratings) < rs.min_rating or max(focus_ratings) > rs.max_rating:
            raise ValueError(f"Ratings must be in min max interval of the related RatingWithFocusSample!")
        return values

    @staticmethod
    def get_type() -> StudyType:
        return StudyType.RATING_WITH_FOCUS
