from typing import TYPE_CHECKING

from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from schemas.composite_assign import CompositeAssignCreate, CompositeAssignView

from .base import BaseModel

if TYPE_CHECKING:
    from models import CompositeTask, Worker
else:
    Worker = object
    CompositeTask = object


class CompositeAssign(BaseModel[CompositeAssignView, CompositeAssignCreate]):
    composite_task: ForeignKeyRelation[CompositeTask] = ForeignKeyField(
        "rendering_server.CompositeTask"
    )
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")

    def to_view(self) -> CompositeAssignView:
        return CompositeAssignView.from_orm(self)
