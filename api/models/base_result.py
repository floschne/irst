from abc import abstractmethod
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

import models
from models import MTurkParams, StudyType


class BaseResult(BaseModel):
    id: str = Field(description="BaseResult UUID", default_factory=uuid)
    sample_id: str = Field(description="UUID of the related BaseSample")
    created: datetime = Field(description="Timestamp of the BaseResult", default_factory=datetime.now)
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('sample_id')
    def sample_must_exist(cls, sample_id: str):
        if models.__validation_disabled__:
            return sample_id.strip()

        from backend.db import RedisHandler
        if not RedisHandler().sample_exists(sample_id=sample_id.strip()):
            raise ValueError(f"Sample '{sample_id}' does not exist!")
        return sample_id.strip()

    @staticmethod
    @abstractmethod
    def get_type() -> StudyType:
        raise NotImplementedError("This method must be overridden in subclasses!")
