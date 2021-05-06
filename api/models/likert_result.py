from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator
from shortuuid import uuid

import models
from models import MTurkParams


class LikertResult(BaseModel):
    id: str = Field(description="LikertResult UUID", default_factory=uuid)
    ls_id: str = Field(description="UUID of the related LikertSample")
    chosen_answer: str = Field(description="Chosen answer")
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('ls_id')
    def likert_sample_must_exist(cls, ls_id: str):
        if models.__validation_disabled__:
            return ls_id.strip()
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.likert_sample_exists(ls_id=ls_id.strip()):
            raise ValueError(f"RankingSample {ls_id} does not exist!")
        return ls_id.strip()

    @root_validator
    def chosen_answer_must_exist(cls, values):
        if models.__validation_disabled__:
            return values

        ls_id = values.get('ls_id')
        chosen_answer = values.get('chosen_answer')
        if ls_id is None or chosen_answer is None:
            raise ValueError(f"ls_id and chosen_answer must not be None!")

        from backend.db import RedisHandler
        redis = RedisHandler()
        ls = redis.load_likert_sample(ls_id=ls_id.strip())
        if chosen_answer not in ls.answers:
            raise ValueError(f"Chosen answer '{chosen_answer}' does not exist in related LikertSample!")
        return values
