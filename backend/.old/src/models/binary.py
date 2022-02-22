from typing import Type, TypeVar

from tortoise.fields.data import TextField

from schemas.binary import BinaryView

from .base import BaseModel

_MODEL = TypeVar("_MODEL", bound="Binary")


class Binary(BaseModel[BinaryView]):
    version: str = TextField()
    url: str = TextField()

    @classmethod
    async def make(cls: Type[_MODEL], version: str, url: str) -> _MODEL:
        return await cls.create(version=version, url=url)

    def to_view(self) -> BinaryView:
        return BinaryView.from_orm(self)
