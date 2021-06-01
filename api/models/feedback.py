from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from shortuuid import uuid


class Feedback(BaseModel):
    id: str = Field(description='User Feedback UUID', default_factory=uuid)
    created: datetime = Field(description="created timestamp", default_factory=datetime.now)
    sample_id: str = Field(description='Sample Id associated with this Feedback')
    message: str = Field(description='The feedback message')
    user_id: Optional[str] = Field(description='Optional User ID that created this Feedback', default=None)
    worker_id: Optional[str] = Field(description='Optional MTurk Worker ID that created this Feedback', default=None)
    hit_id: Optional[str] = Field(description='Optional MTurk HIT ID associated with this Feedback', default=None)
