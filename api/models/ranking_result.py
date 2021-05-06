from typing import List

from pydantic import Field

from models import StudyType
from .base_result import BaseResult


class RankingResult(BaseResult):
    ranking: List[str] = Field(description="User ranking of image IDs related to the RankingSample's query")
    irrelevant: List[str] = Field(
        description="Image IDs which are not related to the RankingSample's query according to the user")

    @staticmethod
    def get_type() -> StudyType:
        return 'ranking'
