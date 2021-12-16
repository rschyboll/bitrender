from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)
from tortoise.functions import Count, Sum

from config import Settings, get_settings
from schemas import FrameView
from utils import save_file
from utils.file import move_file

from .base import BaseModel

if TYPE_CHECKING:
    from models import CompositeTask, Subtask, Task
else:
    Task = object
    Subtask = object
    CompositeTask = object


_MODEL = TypeVar("_MODEL", bound="Frame")


class Frame(BaseModel[FrameView]):
    nr: int = IntField()

    testing: bool = BooleanField(default=False)  # type: ignore
    tested: bool = BooleanField(default=False)  # type: ignore
    distributed: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore

    merged: bool = BooleanField(default=False)  # type: ignore
    merging: bool = BooleanField(default=False)  # type: ignore

    compositing: bool = BooleanField(default=False)  # type: ignore
    composited: bool = BooleanField(default=False)  # type: ignore

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    subtasks: ReverseRelation[Subtask]
    composite_tasks = ReverseRelation[CompositeTask]

    @classmethod
    async def make(cls: Type[_MODEL], task_id: UUID, frame_nr: int) -> _MODEL:
        return await cls.create(task_id=task_id, nr=frame_nr)

    def to_view(self) -> FrameView:
        return FrameView.from_orm(self)

    @property
    def path(self) -> str:
        """Returns the frame render result file path"""
        return get_settings().get_frame_path(self.id)

    @property
    async def rendered_samples(self) -> int:
        """Returns the amount of currently rendered samples"""
        samples = (
            await self.filter(id=self.id)
            .annotate(samples_sum=Sum("subtasks__rendered_samples"))
            .values_list("samples_sum", flat=True)
        )[0]
        if isinstance(samples, int):
            return samples
        return 0

    @property
    async def distributed_samples(self) -> int:
        """Return how many samples have already been distributed"""
        test_samples_list = (
            await self.subtasks.filter(test=True, finished=True, frame_id=self.id)
            .annotate(samples_sum=Sum("rendered_samples"))
            .values_list("samples_sum", flat=True)
        )
        distributed_samples_list = (
            await self.subtasks.filter(test=False, frame_id=self.id)
            .annotate(samples_sum=Sum("max_samples"))
            .values_list("samples_sum", flat=True)
        )
        test_samples = 0
        distributed_samples = 0
        if len(test_samples_list) != 0:
            test_samples_temp = test_samples_list[0]
            if isinstance(test_samples_temp, int):
                test_samples = test_samples_temp
        if len(distributed_samples_list) != 0:
            distributed_samples_temp = distributed_samples_list[0]
            if isinstance(distributed_samples_temp, int):
                distributed_samples = distributed_samples_temp
        return test_samples + distributed_samples

    @property
    async def is_rendered(self) -> bool:
        """Returns if the frame is fully rendered"""
        return await self.rendered_samples == (await self.task).samples

    @property
    async def is_distributed(self) -> bool:
        """Returns if the frame is fully distributed"""
        return await self.distributed_samples == (await self.task).samples

    @property
    async def is_tested(self) -> bool:
        """Returns if the frame has been tested"""
        test_subtask = await self.subtasks.filter(test=True).first()
        if test_subtask is not None:
            return True
        return False

    @property
    async def subtasks_count(self) -> int:
        """Returns on how many subtasks the frame has been splitted"""
        count = (
            await self.subtasks.filter(frame_id=self.id)
            .annotate(subtasks_count=Count("id"))
            .values_list("subtasks_count", flat=True)
        )[0]
        if isinstance(count, int):
            return count
        return 0

    @property
    async def latest_subtask(self) -> Optional[Subtask]:
        """Returns frames latest subtask"""
        return (
            await self.subtasks.filter(frame_id=self.id)
            .order_by("-create_date")
            .first()
        )

    @property
    async def test_subtask(self) -> Subtask:
        """Returns frames test subtask"""
        return await self.subtasks.filter(frame_id=self.id, test=True).get()

    @classmethod
    async def get_not_tested(cls: Type[_MODEL]) -> List[_MODEL]:
        """Returns all not tested frames"""
        return await cls.filter(
            finished=False, testing=False, tested=False, distributed=False, merged=False
        ).select_for_update()

    @classmethod
    async def get_not_distributed(cls: Type[_MODEL]) -> List[_MODEL]:
        """Returns all tested, not distributed frames"""
        return await cls.filter(
            finished=False, tested=True, distributed=False, merged=False
        ).select_for_update()

    @classmethod
    async def get_not_merged(cls: Type[_MODEL]) -> List[_MODEL]:
        return await cls.filter(
            finished=True, tested=True, distributed=True, merged=False, merging=False
        ).select_for_update()

    async def set_merged(self, file: Union[UploadFile, str]) -> None:
        """Sets the frame to be merged and saves the merge result"""
        self.merged = True
        if isinstance(file, str):
            await move_file(file, self.path)
        else:
            await save_file(self.path, file)
        await self.save()

    async def update(self, settings: Settings = get_settings()) -> None:
        if await self.is_rendered:
            self.finished = True
            if await self.subtasks_count == 1:
                subtask = await self.latest_subtask
                if subtask is not None:
                    await self.set_merged(settings.get_subtask_path(subtask.id))
        else:
            self.finished = False
        if await self.is_distributed:
            self.distributed = True
        else:
            self.distributed = False
        if await self.is_tested:
            self.tested = True
        await self.save()
