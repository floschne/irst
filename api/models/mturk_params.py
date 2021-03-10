from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class MTurkParams(BaseModel):
    worker_id: Optional[str] = Query(None, description="MTurk Worker ID")
    assignment_id: Optional[str] = Query(None, description="MTurk Assignment ID")
    hit_id: Optional[str] = Query(None, description="MTurk HIT ID")
