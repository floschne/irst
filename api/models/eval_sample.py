from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator
from shortuuid import uuid


class EvalSample(BaseModel):
    id: str = Field(description='EvalSample UUID', default_factory=uuid)
    created: datetime = Field(description="Timestamp of the result", default_factory=datetime.now)
    gts_id: str = Field(description='GroundTruthSample UUID')
    query: str = Field(description='Query related to the sample')
    image_ids: List[str] = Field(description='Image IDs of the sample')
    image_base_url: str = Field(description='Base URL of the images')

    @validator('gts_id')
    def gts_must_exist(cls, gts_id: str):
        from backend.db import RedisHandler
        redis = RedisHandler()
        if not redis.gt_sample_exists(gts_id=gts_id.strip()):
            raise ValueError(f"GroundTruthSample {gts_id} does not exist!")
        return gts_id.strip()
