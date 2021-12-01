from typing import TYPE_CHECKING, Type, TypeVar, List
from uuid import UUID

from fastapi import UploadFile
from tortoise.fields.data import BooleanField, IntEnumField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneRelation,
    ReverseRelation,
)

from models.composite_assign import CompositeAssign
from models.subtask import SubtaskNotAssigned
from schemas.composite_task import CompositeTaskView, CompositeType, MergeTask
from utils import save_file

from .base import BaseModel

if TYPE_CHECKING:
    from models import Frame, Worker, Subtask
else:
    Worker = object
    Subtask = object
    Frame = object

_MODEL = TypeVar("_MODEL", bound="CompositeTask")


class CompositeTaskAssigned(Exception):
    pass


class CompositeTaskNotAssigned(Exception):
    pass


class CompositeTask(BaseModel[CompositeTaskView]):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")

    type: CompositeType = IntEnumField(CompositeType)

    assigned: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    failed: bool = BooleanField(default=False)  # type: ignore

    worker: OneToOneRelation[Worker]
    assignments: ReverseRelation[CompositeAssign]

    @classmethod
    async def make(
        cls: Type[_MODEL],
        frame_id: UUID,
        composite_type: CompositeType,
    ) -> _MODEL:
        return await cls.create(frame_id=frame_id, type=composite_type)

    def to_view(self) -> CompositeTaskView:
        return CompositeTaskView.from_orm(self)

    @property
    async def merge_data(self) -> List[MergeTask]:
        return [
            {"subtask_id": subtask.id, "samples": subtask.rendered_samples}  # type: ignore
            for subtask in await (await self.frame).subtasks
        ]

    async def assign(self, worker: Worker) -> None:
        if await self.__is_assigned():
            raise CompositeTaskAssigned()
        await self.__create_task_assign(worker)
        await self.__assign(worker)

    async def set_finished(self, file: UploadFile) -> None:
        frame = await self.frame
        if not await self.__is_assigned():
            raise SubtaskNotAssigned()
        self.finished = True
        await self.__deassign()
        await save_file(frame.path, file)
        await self.save()

    async def set_failed(self) -> None:
        if not await self.__is_assigned():
            raise SubtaskNotAssigned()
        self.failed = True
        await self.__deassign()
        await self.save()

    async def __deassign(self) -> None:
        self.assigned = False
        worker = await self.worker
        worker.composite_task = None
        await worker.save()
        await self.save()

    async def __assign(self, worker: Worker) -> None:
        self.assigned = True
        worker.composite_task = self
        await worker.save()
        await self.save()

    async def __is_assigned(self) -> bool:
        return await self.worker is not None or self.assigned

    async def __create_task_assign(self, worker: Worker) -> None:
        await CompositeAssign.make(worker_id=worker.id, task_id=self.id)
