from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from models import BaseModel

if TYPE_CHECKING:
    from models.composite_tasks import CompositeTask
    from models.subtasks import Subtask
    from models.tasks import Task
else:
    Task = object
    Subtask = object
    CompositeTask = object


class Frame(BaseModel):
    nr = IntField()
    running = BooleanField(default=False)
    tested = BooleanField(default=False)
    finished = BooleanField(default=False)
    merged = BooleanField(default=False)
    composited = BooleanField(default=False)

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    subtasks: ReverseRelation[Subtask]
    composite_tasks = ReverseRelation[CompositeTask]
