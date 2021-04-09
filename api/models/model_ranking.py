from typing import Set

from pydantic import BaseModel, Field
from shortuuid import uuid


class ModelRanking(BaseModel):
    id: str = Field(description='ModelRanking UUID', default_factory=uuid)
    ds_id: str = Field(description='ID of the sample in the original dataset')
    query: str = Field(description='Query related to the sample')
    top_k_image_ids: Set[str] = Field(description='IDs of the Top-K ranked images')
