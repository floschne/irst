from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator
from shortuuid import uuid


class EvalResult(BaseModel):
    id: str = Field(description="result uuid", default_factory=uuid)
    sample_id: str = Field(description="UUID of the related EvalSample")
    ranking: List[str] = Field(description="User ranking of images (URLs) related to the EvalSample's query")
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)

    @validator('sample_id')
    def sample_must_exist(cls, sample_id: str):
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.sample_exists(sample_id=sample_id.strip()):
            raise ValueError(f"EvalSample {sample_id} does not exist!")
        return sample_id.strip()
