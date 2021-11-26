from typing import Optional
from uuid import UUID

from .base import BaseCreate, BaseView


class SubtaskView(BaseView):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]
    test: bool

    assigned: bool
    finished: bool
    error: bool


class SubtaskCreate(BaseCreate):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    test: bool
