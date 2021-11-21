from uuid import UUID

from pydantic import BaseModel

from models.composite_tasks import CompositeType


class CompositeTaskView(BaseModel):
    id: UUID
    frame_id: UUID
    type: CompositeType

    assigned: bool
    finished: bool
    error: bool

    class Config:
        orm_mode = True


class CompositeTaskCreate(BaseModel):
    frame_id: UUID
    type: CompositeType
