from typing import List

from pydantic import BaseModel, Field
from shortuuid import uuid


class GroundTruthSample(BaseModel):
    id: str = Field(description='GroundTruthSample UUID', default_factory=uuid)
    query: str = Field(description='Query related to the sample')
    top_k_image_ids: List[str] = Field(description='IDs of the Top-K images')
