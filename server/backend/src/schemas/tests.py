from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestView(BaseModel):
    id: UUID

    start_time: datetime
    end_time: Optional[int]
    samples: Optional[int]
    error: bool
    worker_id: UUID

    class Config:
        orm_mode = True


class TestCreate(BaseModel):
    start_time: datetime
    worker_id: UUID


class TestUpdate(BaseModel):
    id: UUID

    end_time: Optional[datetime]
    samples: Optional[int]
    error: Optional[bool]
