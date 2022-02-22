from typing import TYPE_CHECKING, Type, TypeVar
from uuid import UUID

from tortoise.fields.data import BooleanField, FloatField
from tortoise.fields.relational import ReverseRelation

from schemas.test import TestView

from .base import BaseModel

if TYPE_CHECKING:
    from models.worker import Worker
else:
    Worker = object

_MODEL = TypeVar("_MODEL", bound="Test")


class Test(BaseModel[TestView]):
    sync_time: float = FloatField(null=True, default=None)
    render_time: float = FloatField(null=True, default=None)

    error: bool = BooleanField(default=False)  # type: ignore

    worker: ReverseRelation[Worker]

    @classmethod
    async def make(cls: Type[_MODEL], worker_id: UUID) -> _MODEL:
        return await cls.create(worker_id=worker_id)

    def to_view(self) -> TestView:
        return TestView.from_orm(self)
