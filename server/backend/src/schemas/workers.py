from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class WorkerCreate(BaseModel):
    name: str
    register_date: datetime


class WorkerView(BaseModel):
    id: UUID
    name: str

    register_date: datetime
    active: bool
    test_time: Optional[int]

    class Config:
        orm_mode = True


class WorkerUpdate(BaseModel):
    id: UUID
    name: Optional[str]

    active: Optional[bool]
    test_time: Optional[int]
