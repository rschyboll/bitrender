from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntEnumField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from schemas.composite_task import CompositeTaskCreate, CompositeTaskView, CompositeType

from .base import BaseModel

if TYPE_CHECKING:
    from models.composite_assign import CompositeAssign
    from models.frame import Frame
    from models.worker import Worker
else:
    Worker = object
    CompositeAssign = object
    Frame = object


class CompositeTask(BaseModel[CompositeTaskView, CompositeTaskCreate]):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")

    type: CompositeType = IntEnumField(CompositeType)

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    error: bool = BooleanField(default=False)  # type: ignore

    worker: ReverseRelation[Worker]
    assignments: ReverseRelation[CompositeAssign]

    def to_view(self) -> CompositeTaskView:
        return CompositeTaskView.from_orm(self)
