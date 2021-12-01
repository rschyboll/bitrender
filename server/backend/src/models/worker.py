from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from tortoise.exceptions import DoesNotExist
from tortoise.fields.data import BooleanField, TextField
from tortoise.fields.relational import (
    OneToOneField,
    OneToOneNullableRelation,
    ReverseRelation,
)

from schemas.worker import WorkerView

from .base import BaseModel

if TYPE_CHECKING:
    from models import CompositeAssign, CompositeTask, Subtask, SubtaskAssign, Test
else:
    Test = object
    Subtask = object
    CompositeTask = object
    SubtaskAssign = object
    CompositeAssign = object

_MODEL = TypeVar("_MODEL", bound="Worker")


class Worker(BaseModel[WorkerView]):
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

    @classmethod
    async def make(cls: Type[_MODEL], name: str) -> _MODEL:
        return await cls.create(name=name)

    def to_view(self) -> WorkerView:
        return WorkerView.from_orm(self)

    @property
    async def test_time(self) -> float:
        if self.test is not None:
            test = await self.test
            if test is not None:
                return test.render_time - test.sync_time
        raise DoesNotExist()

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
