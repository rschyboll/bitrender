from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)
from tortoise.functions import Count, Sum

from config import Settings, get_settings
from schemas.frame import FrameCreate, FrameView
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models.composite_task import CompositeTask
    from models.subtask import Subtask
    from models.task import Task
else:
    Task = object
    Subtask = object
    CompositeTask = object


_MODEL = TypeVar("_MODEL", bound="Frame")


class Frame(BaseModel[FrameView, FrameCreate]):
    nr: int = IntField()
    running: bool = BooleanField(default=False)  # type: ignore
    tested: bool = BooleanField(default=False)  # type: ignore
    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    merged: bool = BooleanField(default=False)  # type: ignore
    composited: bool = BooleanField(default=False)  # type: ignore

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    subtasks: ReverseRelation[Subtask]
    composite_tasks = ReverseRelation[CompositeTask]

    def to_view(self) -> FrameView:
        return FrameView.from_orm(self)

    @property
    async def is_finished(self) -> bool:
        frame = (
            await self.annotate(rendered_samples=Sum("samples__rendered_samples"))
            .filter(id=self.id)
            .first()
        )
        if frame is not None:
            return True
        return False

    @property
    async def rendered_samples_sum(self) -> int:
        samples_list = (
            await self.annotate(samples_sum=Sum("subtasks__rendered_samples"))
            .filter(id=self.id)
            .values_list("samples_sum")
        )
        samples = samples_list[0][0]
        if isinstance(samples, int):
            return samples
        raise Exception("rendered_samples_sum working")

    @property
    async def subtasks_count(self) -> int:
        subtasks_list = (
            await self.filter(id=self.id)
            .annotate(subtasks_count=Count("subtasks__id"))
            .values_list("subtasks_count")
        )
        subtasks_count = subtasks_list[0][0]
        if isinstance(subtasks_count, int):
            return subtasks_count
        raise Exception("subtasks_count not working")

    @property
    async def assigned_samples_sum(self) -> int:
        max_not_rendered_samples = await self.filter(subtasks__finished=True).annotate(
            samples_sum=Sum("subtasks__max_samples")
        )
        samples = max_not_rendered_samples[0]
        if isinstance(samples, int):
            return samples + await self.rendered_samples_sum
        raise Exception("assigned_samples_sum not working")

    @classmethod
    async def get_not_tested(cls: Type[_MODEL]) -> List[_MODEL]:
        return await cls.filter(
            finished=False, running=False, tested=False
        ).select_for_update()

    @classmethod
    async def get_not_assigned(cls: Type[_MODEL]) -> List[_MODEL]:
        return await cls.filter(
            finished=False, tested=True, assigned=False
        ).select_for_update()

    async def save_result(
        self, file: UploadFile, settings: Settings = get_settings()
    ) -> None:
        await save_file(settings.get_frame_path(self.id), file)

    async def get_latest_subtask(self) -> Optional[Subtask]:
        return await self.subtasks.order_by("-create_date").first()

    async def get_test_subtask(self) -> Subtask:
        return await self.subtasks.filter(test=True).get()
