from uuid import UUID

from .base import BaseCreate, BaseView


class FrameView(BaseView):
    nr: int

    running: bool
    tested: bool
    finished: bool
    merged: bool
    composited: bool

    task_id: UUID

    class Config:
        orm_mode = True


class FrameCreate(BaseCreate):
    nr: int
    task_id: UUID
