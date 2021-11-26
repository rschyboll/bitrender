from typing import (
    TYPE_CHECKING,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)
from tortoise.functions import Sum

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

    @overload
    @classmethod
    async def get_not_running(
        cls: Type[_MODEL], view: Literal[False] = ...
    ) -> List[_MODEL]:
        ...

    @overload
    @classmethod
    async def get_not_running(
        cls: Type[_MODEL], view: Literal[True]
    ) -> List[FrameView]:
        ...

    @classmethod
    async def get_not_running(
        cls: Type[_MODEL], view: bool = False
    ) -> Union[List[_MODEL], List[FrameView]]:
        if not view:
            return await cls.filter(finished=False, running=False).select_for_update()
        return [
            frame.to_view() for frame in await cls.filter(finished=False, running=False)
        ]

    async def save_result(
        self, file: UploadFile, settings: Settings = get_settings()
    ) -> None:
        await save_file(settings.get_frame_path(self.id), file)

    async def get_latest_subtask(self) -> Optional[Subtask]:
        return await self.subtasks.order_by("-create_date").first()

    async def get_test_subtask(self) -> Subtask:
        return await self.subtasks.filter(test=True).get()

    async def get_samples_sum(self) -> int:
        samples_list = await self.annotate(
            samples_sum=Sum("subtasks__rendered_samples")
        ).values_list("samples_sum")
        samples = samples_list[0]
        if isinstance(samples, int):
            return samples
        raise Exception("get_samples_sum_not_working")
