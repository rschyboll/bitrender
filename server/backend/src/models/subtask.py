# pylint: disable=invalid-name
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from config import Settings, get_settings
from schemas.subtask import SubtaskCreate, SubtaskView
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models.frame import Frame
    from models.subtask_assign import SubtaskAssign
    from models.worker import Worker
else:
    Worker = object
    Frame = object
    SubtaskAssign = object

_MODEL = TypeVar("_MODEL", bound="Subtask")


class Subtask(BaseModel[SubtaskView, SubtaskCreate]):
    seed: int = IntField()
    time_limit: int = IntField()
    max_samples: int = IntField()
    rendered_samples: Optional[int] = IntField(null=True, default=None)
    test: bool = BooleanField()  # type: ignore

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    error: bool = BooleanField(default=False)  # type: ignore

    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")
    worker: ReverseRelation[Worker]
    assignments: ReverseRelation[SubtaskAssign]

    def to_view(self) -> SubtaskView:
        return SubtaskView.from_orm(self)

    @classmethod
    async def get_not_assigned(cls: Type[_MODEL]) -> List[_MODEL]:
        return await cls.filter(assigned=False, finished=False).select_for_update()

    async def save_result(
        self, file: UploadFile, settings: Settings = get_settings()
    ) -> None:
        await save_file(settings.get_subtask_path(self.id), file)

    async def get_latest_assign(self) -> Optional[SubtaskAssign]:
        return (
            await self.assignments.order_by("-create_date").select_for_update().first()
        )
