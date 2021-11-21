from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FrameView(BaseModel):
    id: UUID
    create_date: datetime

    nr: int

    running: bool
    tested: bool
    finished: bool
    merged: bool
    composited: bool

    task_id: UUID

    class Config:
        orm_mode = True


class FrameCreate(BaseModel):
    nr: int
    task_id: UUID


class FrameUpdate(BaseModel):
    id: UUID

    running: bool
    tested: bool
    finished: bool
    merged: bool
    composited: bool
