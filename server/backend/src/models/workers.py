from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, TextField
from tortoise.fields.relational import (
    OneToOneField,
    OneToOneNullableRelation,
    ReverseRelation,
)

from models import BaseModel

if TYPE_CHECKING:
    from models.tests import Test
    from models.subtasks import Subtask
    from models.composite_tasks import CompositeTask
    from models.subtasks_assignments import SubtaskAssignment
    from models.composite_assignments import CompositeAssignment
else:
    Test = object
    Subtask = object
    CompositeTask = object
    SubtaskAssignment = object
    CompositeAssignment = object


class Worker(BaseModel):
    name = TextField()
    active = BooleanField(default=False)

    test: OneToOneNullableRelation[Test] = OneToOneField(
        "rendering_server.Test", null=True, default=None
    )
    subtask: OneToOneNullableRelation[Subtask] = OneToOneField(
        "rendering_server.Subtask",
        null=True,
        default=None,
        related_name="assigned_worker",
    )
    composite_task: OneToOneNullableRelation[CompositeTask] = OneToOneField(
        "rendering_server.CompositeTask", null=True, default=None
    )
    subtask_assignments: ReverseRelation[SubtaskAssignment]
    composite_assignments: ReverseRelation[CompositeAssignment]
