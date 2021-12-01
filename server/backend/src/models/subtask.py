# pylint: disable=invalid-name
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar
from uuid import UUID

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, DatetimeField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneRelation,
    ReverseRelation,
)

from config import get_settings
from models.subtask_assign import SubtaskAssign
from schemas.subtask import SubtaskView
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models import Frame, Worker
else:
    Worker = object
    Frame = object

_MODEL = TypeVar("_MODEL", bound="Subtask")


class SubtaskAssigned(Exception):
    pass


class SubtaskNotAssigned(Exception):
    pass


class Subtask(BaseModel[SubtaskView]):
    samples_offset: int = IntField()
    time_limit: int = IntField()
    max_samples: int = IntField()
    test: bool = BooleanField()  # type: ignore

    progress: int = IntField(default=0)
    rendered_samples: Optional[int] = IntField(null=True, default=None)
    finish_date: datetime = DatetimeField(null=True)

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    failed: bool = BooleanField(default=False)  # type: ignore

    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")
    worker: OneToOneRelation[Worker]
    assignments: ReverseRelation[SubtaskAssign]

    @classmethod
    async def make(
        cls: Type[_MODEL],
        frame_id: UUID,
        samples_offset: int,
        time_limit: int,
        max_samples: int,
        test: bool,
    ) -> _MODEL:
        return await cls.create(
            frame_id=frame_id,
            samples_offset=samples_offset,
            time_limit=time_limit,
            max_samples=max_samples,
            test=test,
        )

    def to_view(self) -> SubtaskView:
        """Creates view schema from subtask"""
        return SubtaskView.from_orm(self)

    @property
    def path(self) -> str:
        """Returns the subtasks render result file path"""
        return get_settings().get_subtask_path(self.id)

    @property
    async def latest_worker(self) -> Optional[Worker]:
        """Returns the latest worker that was assigned to render this subtask"""
        order = "-create_date"
        assign = await self.assignments.order_by(order).select_for_update().first()
        if assign is not None:
            return await assign.worker
        return None

    @classmethod
    async def get_not_assigned(cls: Type[_MODEL]) -> List[_MODEL]:
        """Returns all not assigned subtasks"""
        filters = {"assigned": False, "finished": False, "failed": False}
        return await cls.filter(**filters).select_for_update()

    async def assign(self, worker: Worker) -> None:
        """Assigns subtask to worker"""
        if await self.__is_assigned():
            raise SubtaskAssigned()
        await self.__create_subtask_assign(worker)
        await self.__assign(worker)

    async def set_finished(self, samples: int, file: UploadFile) -> None:
        """Sets subtask as finished and saves the render result"""
        if not await self.__is_assigned():
            raise SubtaskNotAssigned()
        self.finished = True
        self.rendered_samples = samples
        self.finish_date = datetime.now()
        await self.__deassign()
        await save_file(self.path, file)
        await self.save()

    async def set_failed(self) -> None:
        """Sets subtask as failed and deassings it"""
        if not await self.__is_assigned():
            raise SubtaskNotAssigned()
        self.failed = True
        await self.__deassign()
        await self.save()

    async def __deassign(self) -> None:
        self.assigned = False
        worker = await self.worker
        worker.subtask = None
        await worker.save()
        await self.save()

    async def __assign(self, worker: Worker) -> None:
        self.assigned = True
        worker.subtask = self
        await worker.save()
        await self.save()

    async def __is_assigned(self) -> bool:
        return await self.worker is not None or self.assigned

    async def __create_subtask_assign(self, worker: Worker) -> None:
        await SubtaskAssign(worker_id=worker.id, subtask_id=self.id).save()
