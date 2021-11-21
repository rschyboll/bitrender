from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class WorkerCreate(BaseModel):
    name: str


class WorkerView(BaseModel):
    id: UUID
    create_date: datetime

    name: str
    active: bool

    subtask_id: Optional[UUID]
    test_id: Optional[UUID]
    composite_task_id: Optional[UUID]

    class Config:
        orm_mode = True


class WorkerUpdate(BaseModel):
    id: UUID

    active: Optional[bool]

    test_id: Optional[UUID]
    subtask_id: Optional[UUID]
    composite_task_id: Optional[UUID]
