from pydantic import Field, root_validator

import models
from models import StudyType
from .base_result import BaseResult


class LikertResult(BaseResult):
    chosen_answer: str = Field(description="Chosen answer")

    @root_validator
    def chosen_answer_must_exist(cls, values):
        if models.__validation_disabled__:
            return values

        sample_id = values.get('sample_id')
        chosen_answer = values.get('chosen_answer')
        if sample_id is None or chosen_answer is None:
            raise ValueError(f"sample_id and chosen_answer must not be None!")

        from backend.db import RedisHandler
        ls = RedisHandler().load_likert_sample(ls_id=sample_id.strip())
        if chosen_answer not in ls.answers:
            raise ValueError(f"Chosen answer '{chosen_answer}' does not exist in related LikertSample!")
        return values

    @staticmethod
    def get_type() -> StudyType:
        return StudyType.LIKERT
