from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel, Field, validator
from shortuuid import uuid

import models
from models import MTurkParams, StudyType


class BaseSample(BaseModel):
    id: str = Field(description='BaseSample UUID', default_factory=uuid)
    mr_id: str = Field(description='ID of the related ModelRanking')
    mt_params: Optional[MTurkParams] = Field(description="Optional MTurk Parameters", default=None)

    @validator('mr_id')
    def mr_must_exist(cls, mr_id: str):
        from backend.db import RedisHandler
        if models.__validation_disabled__:
            return mr_id.strip()

        if not RedisHandler().model_ranking_exists(mr_id=mr_id.strip()):
            raise ValueError(f"ModelRanking {mr_id} does not exist!")
        return mr_id.strip()

    def add_mt_params(self, mt: MTurkParams):
        self.mt_params = mt

    @staticmethod
    @abstractmethod
    def get_type() -> StudyType:
        raise NotImplementedError("This method must be overridden in subclasses!")
