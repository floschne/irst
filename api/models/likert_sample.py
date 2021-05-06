from typing import List

from pydantic import Field, validator

from models import StudyType
from .base_sample import BaseSample


class LikertSample(BaseSample):
    caption: str = Field(description='Caption related to the image IDs')
    image_ids: List[str] = Field(description='Image IDs of the LikertSample')
    question: str = Field(description="Question that should be answered")
    answers: List[str] = Field(description="List of the answers of the Likert-Scale",
                               default=['strongly agree', 'agree', 'neutral', 'disagree', 'strongly disagree'])
    answer_weights: List[int] = Field(description="List of the weights of the answers of the Likert-Scale",
                                      default=[2, 1, 0, -1, -2])

    @validator('caption')
    def caption_must_not_be_empty(cls, caption: str):
        if len(caption) == 0:
            raise ValueError(f"The caption must not be empty!")
        return caption.strip()

    @validator('image_ids')
    def image_ids_must_not_be_empty(cls, image_ids: List[str]):
        if len(image_ids) == 0:
            raise ValueError(f"The images ids must not be empty!")
        return image_ids

    @staticmethod
    def get_type() -> StudyType:
        return StudyType.LIKERT
