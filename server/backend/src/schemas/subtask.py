from typing import Optional
from uuid import UUID

from .base import BaseCreate, BaseView


class SubtaskView(BaseView):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]

    assigned: bool
    finished: bool
    error: bool


class SubtaskCreate(BaseCreate):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
