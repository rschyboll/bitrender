from tortoise.fields.data import TextField

from schemas.binary import BinaryCreate, BinaryView

from .base import BaseModel


class Binary(BaseModel[BinaryView, BinaryCreate]):
    version: str = TextField()
    url: str = TextField()

    def to_view(self) -> BinaryView:
        return BinaryView.from_orm(self)
