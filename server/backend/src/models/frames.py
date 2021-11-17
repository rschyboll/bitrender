from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from models import BaseModel

if TYPE_CHECKING:
    from models.tasks import Task
    from models.subtasks import Subtask
else:
    Task = object
    Subtask = object


class Frame(BaseModel):
    nr = IntField()
    finished = BooleanField(default=False)

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    subtasks: ReverseRelation[Subtask]
