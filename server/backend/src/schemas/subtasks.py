from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubtaskCreate(BaseModel):
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]
    finished: bool = False


class SubtaskView(BaseModel):
    id: UUID
    frame_id: UUID
    seed: int
    time_limit: int
    max_samples: int
    rendered_samples: Optional[int]
    finished: bool

    class Config:
        orm_mode = True
