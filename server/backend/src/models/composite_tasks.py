from enum import IntEnum
from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntEnumField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from models import BaseModel

if TYPE_CHECKING:
    from models.composite_assignments import CompositeAssignment
    from models.frames import Frame
    from models.workers import Worker
else:
    Worker = object
    CompositeAssignment = object
    Frame = object


class CompositeType(IntEnum):
    COMPOSITE = 1
    MERGE = 2


class CompositeTask(BaseModel):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")

    type: CompositeType = IntEnumField(CompositeType)

    assigned = BooleanField(default=False)
    finished = BooleanField(default=False)
    error = BooleanField(default=False)

    worker = ReverseRelation[Worker]
    assignments = ReverseRelation[CompositeAssignment]
