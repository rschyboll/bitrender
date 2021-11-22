from typing import TYPE_CHECKING, List, Optional, Type, TypeVar
from uuid import UUID

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)
from config import Settings, get_settings

from models.base import BaseModel
from schemas.subtasks import SubtaskCreate, SubtaskView
from utils import save_file

if TYPE_CHECKING:
    from models.frames import Frame
    from models.subtasks_assignments import SubtaskAssignment
    from models.workers import Worker
else:
    Worker = object
    Frame = object
    SubtaskAssignment = object

T = TypeVar("T", bound="Subtask")  # pylint: disable=invalid-name


class Subtask(BaseModel):
    seed: int = IntField()
    time_limit: int = IntField()
    max_samples: int = IntField()
    rendered_samples: Optional[int] = IntField(null=True, default=None)

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    error: bool = BooleanField(default=False)  # type: ignore

    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")
    worker = ReverseRelation[Worker]
    assignments = ReverseRelation[SubtaskAssignment]

    @classmethod
    async def get_lock(cls: Type[T]) -> List[T]:
        return await cls.select_for_update()

    @classmethod
    async def get_view(cls: Type[T]) -> List[SubtaskView]:
        return [subtask.to_view() for subtask in await cls.all()]

    @classmethod
    async def get_lock_by_id(cls: Type[T], subtask_id: UUID) -> T:
        return await cls.select_for_update().get(id=subtask_id)

    @classmethod
    async def get_view_by_id(cls: Type[T], subtask_id: UUID) -> T:
        return await cls.get(id=subtask_id)

    @classmethod
    async def get_lock_not_assigned(cls: Type[T]) -> List[T]:
        return await cls.filter(assigned=False, finished=False).select_for_update()

    @classmethod
    async def from_create(cls: Type[T], subtask_create: SubtaskCreate) -> T:
        subtask = cls(**subtask_create.dict())
        await subtask.save()
        return subtask

    def to_view(self) -> SubtaskView:
        return SubtaskView.from_orm(self)

    async def save_result(
        self, file: UploadFile, settings: Settings = get_settings()
    ) -> None:
        await save_file(settings.get_subtask_path(self.id), file)
