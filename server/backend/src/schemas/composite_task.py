from enum import IntEnum
from uuid import UUID

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
