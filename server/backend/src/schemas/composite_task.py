from enum import IntEnum
from typing import List, TypedDict
from uuid import UUID

from pydantic.main import BaseModel

from .base import BaseCreate, BaseView


class CompositeType(IntEnum):
    COMPOSITE = 1
    MERGE = 2


class CompositeTaskView(BaseView):
    type: CompositeType

    assigned: bool
    finished: bool
    error: bool


class CompositeTaskCreate(BaseCreate):
    frame_id: UUID
    type: CompositeType


class MergeTask(TypedDict):
    samples: int
    subtask_id: UUID


class MergeTaskData(BaseModel):
    composite_task_id: UUID
    subtask_data: List[MergeTask]
