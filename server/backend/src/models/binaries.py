from uuid import UUID
from typing import TypeVar, Type, List, Optional

from tortoise.fields.data import TextField

from models.base import BaseModel
from schemas.binaries import BinaryView, BinaryCreate

T = TypeVar("T", bound="Binary")  # pylint: disable=invalid-name


class Binary(BaseModel):
    version: str = TextField()
    url: str = TextField()

    @classmethod
    async def get_lock(cls: Type[T]) -> List[T]:
        return await cls.select_for_update()

    @classmethod
    async def get_view(cls: Type[T]) -> List[BinaryView]:
        return [binary.to_view() for binary in await cls.all()]

    @classmethod
    async def get_lock_by_id(cls: Type[T], binary_id: UUID) -> T:
        return await cls.get(id=binary_id)

    @classmethod
    async def get_view_by_id(cls: Type[T], binary_id: UUID) -> BinaryView:
        return (await cls.get(id=binary_id)).to_view()

    @classmethod
    async def get_lock_latest(cls: Type[T]) -> Optional[T]:
        return await cls.all().order_by("-create_date").first()

    @classmethod
    async def from_create(cls: Type[T], binary_create: BinaryCreate) -> T:
        binary = cls(**binary_create.dict())
        await binary.save()
        return binary

    def to_view(self) -> BinaryView:
        return BinaryView.from_orm(self)
