from typing import List

from pydantic import BaseModel, Field
from shortuuid import uuid


class GroundTruthSample(BaseModel):
    id: str = Field(description='GroundTruthSample UUID', default_factory=uuid)
    ds_id: str = Field(description='ID of the sample in the original dataset')
    query: str = Field(description='Query related to the sample')
    top_k_image_ids: List[str] = Field(description='IDs of the Top-K images')
