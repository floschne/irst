from typing import List

from pydantic import Field

from models import StudyType
from .base_sample import BaseSample


class RatingWithFocusSample(BaseSample):
    image_ids: List[str] = Field(description='Image IDs of the RatingWithFocusSample')
    caption: str = Field(description='The caption of the RatingWithFocusSample')
    focus: str = Field(description='The focus of the RatingWithFocusSample')
    min_rating: float = Field(description='Minimum rating of a single image', default=0.0)
    max_rating: float = Field(description='Maximum rating of a single image', default=5.0)
    rating_step: float = Field(description='Step size of the rating', default=1.0)

    @staticmethod
    def get_type() -> StudyType:
        return StudyType.RATING_WITH_FOCUS
