from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator
from shortuuid import uuid


class EvalSample(BaseModel):
    id: str = Field(description='EvalSample UUID', default_factory=uuid)
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    mr_id: str = Field(description='ModelRanking UUID')
    query: str = Field(description='Query related to the sample')
    image_ids: List[str] = Field(description='Image IDs of the sample')

    @validator('mr_id')
    def mr_must_exist(cls, mr_id: str):
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.model_ranking_exists(mr_id=mr_id.strip()):
            raise ValueError(f"ModelRanking {mr_id} does not exist!")
        return mr_id.strip()
