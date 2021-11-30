from typing import TYPE_CHECKING, Type, TypeVar
from uuid import UUID

from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from schemas.subtask_assign import SubtaskAssignView

from .base import BaseModel

if TYPE_CHECKING:
    from models import Subtask, Worker
else:
    Worker = object
    Subtask = object

_MODEL = TypeVar("_MODEL", bound="SubtaskAssign")


class SubtaskAssign(BaseModel[SubtaskAssignView]):
    subtask: ForeignKeyRelation[Subtask] = ForeignKeyField(
        "rendering_server.Subtask", related_name="assignments"
    )
    worker: ForeignKeyRelation[Worker] = ForeignKeyField(
        "rendering_server.Worker", related_name="subtask_assigns"
    )

    @classmethod
    async def make(cls: Type[_MODEL], subtask_id: UUID, worker_id: UUID) -> _MODEL:
        return await cls.create(subtask_id=subtask_id, worker_id=worker_id)

    def to_view(self) -> SubtaskAssignView:
        return SubtaskAssignView.from_orm(self)
