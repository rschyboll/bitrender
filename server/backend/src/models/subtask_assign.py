from typing import TYPE_CHECKING

from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from schemas.subtask_assign import SubtaskAssignCreate, SubtaskAssignView

from .base import BaseModel

if TYPE_CHECKING:
    from models.subtask import Subtask
    from models.worker import Worker
else:
    Worker = object
    Subtask = object


class SubtaskAssign(BaseModel[SubtaskAssignView, SubtaskAssignCreate]):
    subtask: ForeignKeyRelation[Subtask] = ForeignKeyField("rendering_server.Subtask")
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")

    def to_view(self) -> SubtaskAssignView:
        return SubtaskAssignView.from_orm(self)
