from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, TextField
from tortoise.fields.relational import (
    OneToOneField,
    OneToOneNullableRelation,
    ReverseRelation,
)

from schemas.worker import WorkerCreate, WorkerView

from .base import BaseModel

if TYPE_CHECKING:
    from models.composite_assign import CompositeAssign
    from models.composite_task import CompositeTask
    from models.subtask import Subtask
    from models.subtask_assign import SubtaskAssign
    from models.test import Test
else:
    Test = object
    Subtask = object
    CompositeTask = object
    SubtaskAssign = object
    CompositeAssign = object


class Worker(BaseModel[WorkerView, WorkerCreate]):
    name = TextField()
    active = BooleanField(default=False)

    test: OneToOneNullableRelation[Test] = OneToOneField(
        "rendering_server.Test", null=True, default=None
    )
    subtask: OneToOneNullableRelation[Subtask] = OneToOneField(
        "rendering_server.Subtask", null=True, default=None
    )
    composite_task: OneToOneNullableRelation[CompositeTask] = OneToOneField(
        "rendering_server.CompositeTask", null=True, default=None
    )
    subtask_assignments: ReverseRelation[SubtaskAssign]
    composite_assignments: ReverseRelation[CompositeAssign]

    def to_view(self) -> WorkerView:
        return WorkerView.from_orm(self)
