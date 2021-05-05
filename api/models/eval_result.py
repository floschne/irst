from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

from models import MTurkParams
import models


class EvalResult(BaseModel):
    id: str = Field(description="result uuid", default_factory=uuid)
    es_id: str = Field(description="UUID of the related EvalSample")
    ranking: List[str] = Field(description="User ranking of image ids related to the EvalSample's query")
    irrelevant: List[str] = Field(description="Image ids which are not related to the EvalSample's query according to the user")
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('es_id')
    def eval_sample_must_exist(cls, sample_id: str):
        if models.__validation_disabled__:
            return sample_id.strip()
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.eval_sample_exists(sample_id=sample_id.strip()):
            raise ValueError(f"EvalSample {sample_id} does not exist!")
        return sample_id.strip()
