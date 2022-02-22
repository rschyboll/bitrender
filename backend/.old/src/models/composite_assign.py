from typing import TYPE_CHECKING, Type, TypeVar
from uuid import UUID

from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from schemas.composite_assign import CompositeAssignView

from .base import BaseModel

if TYPE_CHECKING:
    from models import CompositeTask, Worker
else:
    Worker = object
    CompositeTask = object

_MODEL = TypeVar("_MODEL", bound="CompositeAssign")


class CompositeAssign(BaseModel[CompositeAssignView]):
    task: ForeignKeyRelation[CompositeTask] = ForeignKeyField(
        "rendering_server.CompositeTask"
    )
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")

    @classmethod
    async def make(cls: Type[_MODEL], task_id: UUID, worker_id: UUID) -> _MODEL:
        return await cls.create(task_id=task_id, worker_id=worker_id)

    def to_view(self) -> CompositeAssignView:
        return CompositeAssignView.from_orm(self)
