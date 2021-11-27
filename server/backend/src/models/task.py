from typing import TYPE_CHECKING, Type, TypeVar

from tortoise.fields.data import BooleanField, IntField, TextField
from tortoise.fields.relational import ReverseRelation
from tortoise.functions import Count
from tortoise.transactions import atomic

from config import Settings, get_settings
from schemas.task import TaskCreate, TaskView
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models.frame import Frame
else:
    Frame = object
_MODEL = TypeVar("_MODEL", bound="Task")


class Task(BaseModel[TaskView, TaskCreate]):
    name: str = TextField()
    samples: int = IntField()
    start_frame: int = IntField()
    end_frame: int = IntField()
    resolution_x: int = IntField()
    resolution_y: int = IntField()

    finished: bool = BooleanField(default=False)  # type: ignore

    frames: ReverseRelation[Frame]

    def to_view(self) -> TaskView:
        return TaskView.from_orm(self)

    @property
    async def finished_frames_count(self) -> int:
        frame_list = (
            await self.filter(id=self.id, frames__merged=True)
            .annotate(frame_count=Count("frames__id"))
            .values_list("frame_count")
        )
        frame_count = frame_list[0][0]
        if isinstance(frame_count, int):
            return frame_count
        raise Exception("finished_frames_count not working")

    @classmethod
    @atomic()
    async def from_create(
        cls: Type[_MODEL], create: TaskCreate, settings: Settings = get_settings()
    ) -> _MODEL:
        task = cls(**create.dict(), name=create.file.filename)
        await task.save()
        await save_file(settings.get_task_path(task.id), create.file)
        return task
