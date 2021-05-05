from typing import List, Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

import models
from models import MTurkParams


class LikertSample(BaseModel):
    id: str = Field(description="LikertSample UUID", default_factory=uuid)
    mr_id: str = Field(description="UUID of the related ModelRanking")
    question: str = Field(description="Question that should be answered")
    image_ids: List[str] = Field(description='Image IDs of the sample')
    answers: List[str] = Field(description="List of the answers of the Likert-Scale",
                               default=['strongly agree', 'agree', 'neutral', 'disagree', 'strongly disagree'])
    answer_weights: List[int] = Field(description="List of the weights of the answers of the Likert-Scale",
                                      default=[2, 1, 0, -1, -2])
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('mr_id')
    def model_ranking_must_exist(cls, mr_id: str):
        if models.__validation_disabled__:
            return mr_id.strip()
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.model_ranking_exists(mr_id=mr_id.strip()):
            raise ValueError(f"ModelRanking {mr_id} does not exist!")
        return mr_id.strip()
