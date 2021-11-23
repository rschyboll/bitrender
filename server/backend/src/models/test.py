from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, FloatField
from tortoise.fields.relational import ReverseRelation

from schemas.test import TestCreate, TestView

from .base import BaseModel

if TYPE_CHECKING:
    from models.worker import Worker
else:
    Worker = object


class Test(BaseModel[TestView, TestCreate]):
    sync_time: float = FloatField(null=True, default=None)
    render_time: float = FloatField(null=True, default=None)

    error: bool = BooleanField(default=False)  # type: ignore

    worker: ReverseRelation[Worker]

    def to_view(self) -> TestView:
        return TestView.from_orm(self)
