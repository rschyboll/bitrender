from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)
from tortoise.functions import Sum

from models import BaseModel
from schemas.frames import FrameView

if TYPE_CHECKING:
    from models.composite_tasks import CompositeTask
    from models.subtasks import Subtask
    from models.tasks import Task
else:
    Task = object
    Subtask = object
    CompositeTask = object


class Frame(BaseModel):
    nr: int = IntField()
    running: bool = BooleanField(default=False)  # type: ignore
    tested: bool = BooleanField(default=False)  # type: ignore
    finished: bool = BooleanField(default=False)  # type: ignore
    merged: bool = BooleanField(default=False)  # type: ignore
    composited: bool = BooleanField(default=False)  # type: ignore

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    subtasks: ReverseRelation[Subtask]
    composite_tasks = ReverseRelation[CompositeTask]

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

    def to_view(self) -> FrameView:
        return FrameView.from_orm(self)
