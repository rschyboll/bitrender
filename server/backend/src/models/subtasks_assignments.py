from typing import TYPE_CHECKING

from tortoise.fields.relational import ForeignKeyRelation, ForeignKeyField

from models import BaseModel

if TYPE_CHECKING:
    from models.workers import Worker
    from models.subtasks import Subtask
else:
    Worker = object
    Subtask = object


class SubtaskAssignment(BaseModel):
    subtask: ForeignKeyRelation[Subtask] = ForeignKeyField("rendering_server.Subtask")
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")
