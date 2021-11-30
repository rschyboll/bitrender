from typing import TYPE_CHECKING, Type, TypeVar
from uuid import UUID

from tortoise.fields.data import BooleanField, IntEnumField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from schemas.composite_task import CompositeTaskView, CompositeType

from .base import BaseModel

if TYPE_CHECKING:
    from models import CompositeAssign, Frame, Worker
else:
    Worker = object
    CompositeAssign = object
    Frame = object

_MODEL = TypeVar("_MODEL", bound="CompositeTask")


class CompositeTask(BaseModel[CompositeTaskView]):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")

    type: CompositeType = IntEnumField(CompositeType)

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    error: bool = BooleanField(default=False)  # type: ignore

    worker: ReverseRelation[Worker]
    assignments: ReverseRelation[CompositeAssign]

    @classmethod
    async def make(
        cls: Type[_MODEL],
        frame_id: UUID,
        composite_type: CompositeType,
    ) -> _MODEL:
        return await cls.create(frame_id=frame_id, type=composite_type)

    def to_view(self) -> CompositeTaskView:
        return CompositeTaskView.from_orm(self)
