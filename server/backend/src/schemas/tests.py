from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestView(BaseModel):
    id: UUID

    start_time: datetime
    end_time: Optional[datetime]

    sync_time: Optional[float]
    render_time: Optional[float]
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

    sync_time: Optional[float]
    render_time: Optional[float]
    error: Optional[bool]
