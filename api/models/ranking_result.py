from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

from models import MTurkParams
import models


class RankingResult(BaseModel):
    id: str = Field(description="result uuid", default_factory=uuid)
    rs_id: str = Field(description="UUID of the related RankingSample")
    ranking: List[str] = Field(description="User ranking of image ids related to the RankingSample's query")
    irrelevant: List[str] = Field(description="Image ids which are not related to the RankingSample's query according to the user")
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('rs_id')
    def ranking_sample_must_exist(cls, rs_id: str):
        if models.__validation_disabled__:
            return rs_id.strip()
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.ranking_sample_exists(rs_id=rs_id.strip()):
            raise ValueError(f"RankingSample {rs_id} does not exist!")
        return rs_id.strip()
