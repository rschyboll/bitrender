from typing import Optional
from uuid import UUID

from .base import BaseCreate, BaseView


class WorkerCreate(BaseCreate):
    name: str


class WorkerView(BaseView):
    name: str
    active: bool

    subtask_id: Optional[UUID]
    test_id: Optional[UUID]
    composite_task_id: Optional[UUID]
