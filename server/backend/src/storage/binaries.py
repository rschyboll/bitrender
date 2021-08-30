from typing import List
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from models.binaries import Binary
from schemas.binaries import BinaryCreate, BinaryView


async def create(binary: BinaryCreate) -> BinaryView:
    binary_db = Binary(**binary.dict())
    await binary_db.save()
    return BinaryView.from_orm(binary_db)


async def get() -> List[BinaryView]:
    binaries = await Binary.all()
    binary_views: List[BinaryView] = []
    for binary in binaries:
        binary_views.append(BinaryView.from_orm(binary))
    return binary_views


async def get_by_id(binary_id: UUID) -> BinaryView:
    binary_db = await Binary.get(id=binary_id)
    return BinaryView.from_orm(binary_db)


async def get_latest() -> BinaryView:
    binary_db = await Binary.all().order_by("-id").first()
    if binary_db is None:
        raise DoesNotExist
    return BinaryView.from_orm(binary_db)


async def delete(binary_id: UUID) -> None:
    binary_db = await Binary.get(id=binary_id)
    await binary_db.delete()
