from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

from models import MTurkParams
import models


class RankingSample(BaseModel):
    id: str = Field(description='RankingSample UUID', default_factory=uuid)
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    mr_id: str = Field(description='ModelRanking UUID')
    query: str = Field(description='Query related to the sample')
    image_ids: List[str] = Field(description='Image IDs of the sample')
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('mr_id')
    def mr_must_exist(cls, mr_id: str):
        if models.__validation_disabled__:
            return mr_id.strip()

        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.model_ranking_exists(mr_id=mr_id.strip()):
            raise ValueError(f"ModelRanking {mr_id} does not exist!")
        return mr_id.strip()

    def add_mt_params(self, mt: MTurkParams):
        self.mt_params = mt
