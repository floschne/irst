from typing import List

from pydantic import Field

from models import StudyType
from .base_sample import BaseSample


class RankingSample(BaseSample):
    query: str = Field(description='Query related to the RankingSample')
    image_ids: List[str] = Field(description='Image IDs of the RankingSample')

    @staticmethod
    def get_type() -> StudyType:
        return 'ranking'
