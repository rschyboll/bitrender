from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from .base import BaseCreate, BaseView


class SubtaskView(BaseView):
    frame_id: UUID
    samples_offset: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]
    test: bool

    assigned: bool
    finished: bool
    error: bool


class SubtaskCreate(BaseCreate):
    frame_id: UUID
    samples_offset: int
    time_limit: int
    max_samples: int
    test: bool


class SubtaskData(BaseModel):
    task_id: UUID
    subtask_id: UUID
    frame_nr: int
    samples_offset: int
    time_limit: int
    max_samples: int
    resolution_x: int
    resolution_y: int
