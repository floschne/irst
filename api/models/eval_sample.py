from typing import List

from pydantic import BaseModel, Field
from shortuuid import uuid


class EvalSample(BaseModel):
    id: str = Field(description='sample uuid', default_factory=uuid)
    query: str = Field(description='Query related to the sample')
    top_k: List[str] = Field(description='URLs of the top-k matching images of the query predicted by a model')
    random: List[str] = Field(description='URLs of random images not related to the query')
