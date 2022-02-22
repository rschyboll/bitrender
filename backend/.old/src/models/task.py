import os
from typing import TYPE_CHECKING, Type, TypeVar, List
from zipfile import ZipFile

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField, TextField
from tortoise.fields.relational import ReverseRelation
from tortoise.functions import Count

from config import Settings, get_settings
from schemas.task import TaskView
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models.frame import Frame
else:
    Frame = object

_MODEL = TypeVar("_MODEL", bound="Task")


class Task(BaseModel[TaskView]):
    name: str = TextField()
    samples: int = IntField()
    start_frame: int = IntField()
    end_frame: int = IntField()
    resolution_x: int = IntField()
    resolution_y: int = IntField()

    finished: bool = BooleanField(default=False)  # type: ignore
    packed: bool = BooleanField(default=False)  # type: ignore

    frames: ReverseRelation[Frame]

    @classmethod
    async def make(
        cls: Type[_MODEL],
        file: UploadFile,
        samples: int,
        start_frame: int,
        end_frame: int,
        resolution_x: int,
        resolution_y: int,
        settings: Settings = get_settings(),
    ) -> _MODEL:
        task = await cls.create(
            name=file.filename,
            samples=samples,
            start_frame=start_frame,
            end_frame=end_frame,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
        )
        await save_file(settings.get_task_path(task.id), file)
        return task

    def to_view(self) -> TaskView:
        return TaskView.from_orm(self)

    @property
    def path(self) -> str:
        return get_settings().get_task_path(self.id)

    @property
    def zip_path(self) -> str:
        return get_settings().get_task_path(self.id) + ".zip"

    @property
    async def finished_frames_count(self) -> int:
        frame_list = (
            await self.filter(id=self.id, frames__merged=True)
            .annotate(frame_count=Count("frames__id"))
            .values_list("frame_count", flat=True)
        )
        if len(frame_list) == 0:
            return 0
        frame_count = frame_list[0]
        if isinstance(frame_count, int):
            return frame_count
        return 0

    @classmethod
    async def get_finished_not_packed(cls: Type[_MODEL]) -> List[_MODEL]:
        return await cls.filter(finished=True, packed=False).select_for_update()

    async def update(self) -> None:
        if await self.finished_frames_count == self.end_frame + 1 - self.start_frame:
            self.finished = True
        await self.save()

    async def pack(self) -> None:
        frames = await self.frames
        with ZipFile(self.zip_path, "w") as file:
            for frame in frames:
                file.write(frame.path, arcname=str(frame.nr) + ".exr")
                os.remove(frame.path)
        self.packed = True
        await self.save()
