from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

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

_MODEL = TypeVar("_MODEL", bound="Worker")


class Worker(BaseModel[WorkerView, WorkerCreate]):
    name: str = TextField()
    active: bool = BooleanField(default=False)  # type: ignore

    test: OneToOneNullableRelation[Test] = OneToOneField(
        "rendering_server.Test", null=True, default=None
    )
    subtask: OneToOneNullableRelation[Subtask] = OneToOneField(
        "rendering_server.Subtask", null=True, default=None
    )
    composite_task: OneToOneNullableRelation[CompositeTask] = OneToOneField(
        "rendering_server.CompositeTask", null=True, default=None
    )
    subtask_assigns: ReverseRelation[SubtaskAssign]
    composite_assigns: ReverseRelation[CompositeAssign]

    def to_view(self) -> WorkerView:
        return WorkerView.from_orm(self)

    @classmethod
    async def get_idle(cls: Type[_MODEL]) -> List[_MODEL]:
        return (
            await cls.filter(subtask=None, composite_task=None, active=True)
            .filter(test__render_time__isnull=False)
            .order_by("test__render_time")
            .select_for_update()
        )

    async def get_test(self) -> Optional[Test]:
        if self.test is not None:
            return await self.test
        return None
