from typing import TYPE_CHECKING, Literal, Type, TypeVar, Union, overload
from uuid import UUID

from tortoise.fields.data import BooleanField, IntField, TextField
from tortoise.fields.relational import ReverseRelation
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
    name = TextField()
    samples = IntField()
    start_frame = IntField()
    end_frame = IntField()
    resolution_x = IntField()
    resolution_y = IntField()

    finished = BooleanField(default=False)

    frames: ReverseRelation[Frame]

    def to_view(self) -> TaskView:
        return TaskView.from_orm(self)

    @atomic()
    @classmethod
    async def from_create(
        cls: Type[_MODEL], create: TaskCreate, settings: Settings = get_settings()
    ) -> _MODEL:
        task = cls(**create.dict(), name=create.file.filename)
        await task.save()
        await save_file(settings.get_task_path(task.id), create.file)
        return task

    @overload
    @classmethod
    async def get_by_frame_id(
        cls: Type[_MODEL], frame_id: UUID, view: Literal[False] = ...
    ) -> _MODEL:
        ...

    @overload
    @classmethod
    async def get_by_frame_id(
        cls: Type[_MODEL], frame_id: UUID, view: Literal[True]
    ) -> TaskView:
        ...

    @classmethod
    async def get_by_frame_id(
        cls: Type[_MODEL], frame_id: UUID, view: bool = False
    ) -> Union[_MODEL, TaskView]:
        if not view:
            return await cls.select_for_update().get(frames__id=frame_id)
        return (await cls.get(frames__id=frame_id)).to_view()

    @overload
    @classmethod
    async def get_by_subtask_id(
        cls: Type[_MODEL], subtask_id: UUID, view: Literal[False] = ...
    ) -> _MODEL:
        ...

    @overload
    @classmethod
    async def get_by_subtask_id(
        cls: Type[_MODEL], subtask_id: UUID, view: Literal[True]
    ) -> TaskView:
        ...

    @classmethod
    async def get_by_subtask_id(
        cls: Type[_MODEL], subtask_id: UUID, view: bool = False
    ) -> Union[_MODEL, TaskView]:
        if not view:
            return await cls.select_for_update().get(frames__subtasks__id=subtask_id)
        return (await cls.get(frames__subtasks__id=subtask_id)).to_view()
