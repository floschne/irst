from datetime import datetime

from pydantic import BaseModel, Field
from shortuuid import uuid


class Feedback(BaseModel):
    id: str = Field(description='User Feedback UUID', default_factory=uuid)
    created: datetime = Field(description="created timestamp", default_factory=datetime.now)
    rs_id: str = Field(description='RankingSample ID associated with this Feedback')
    message: str = Field(description='The feedback message')
    worker_id: str = Field(description='Optional MTurk Worker ID that created this Feedback', default=None)
    hit_id: str = Field(description='Optional MTurk HIT ID associated with this Feedback', default=None)
