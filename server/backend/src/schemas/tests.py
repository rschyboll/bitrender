from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestView(BaseModel):
    id: UUID
    create_date: datetime

    sync_time: Optional[float]
    render_time: Optional[float]
    error: bool

    class Config:
        orm_mode = True


class TestCreate(BaseModel):
    worker_id: UUID


class TestUpdate(BaseModel):
    id: UUID

    end_time: Optional[datetime]
    sync_time: Optional[float]
    render_time: Optional[float]
    error: Optional[bool]
