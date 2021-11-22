from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubtaskView(BaseModel):
    id: UUID
    create_date: datetime

    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]

    assigned: bool
    finished: bool
    error: bool

    class Config:
        orm_mode = True


class SubtaskCreate(BaseModel):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
