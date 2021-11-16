from uuid import UUID

from pydantic import BaseModel


class FrameCreate(BaseModel):
    nr: int
    finished: bool = False

    task_id: UUID


class FrameView(BaseModel):
    id: UUID
    nr: int
    finished: bool

    task_id: UUID

    class Config:
        orm_mode = True
