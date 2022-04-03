"""This module contains the base class for all database models."""
from datetime import datetime
from typing import TYPE_CHECKING, Type, TypeVar
from uuid import UUID

from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model

if TYPE_CHECKING:
    from bitrender.base.auth import AclEntry
else:
    AclEntry = object

_MODEL = TypeVar("_MODEL", bound="BaseModel")


class BaseModel(Model):
    """TODO generate docstring"""

    id: UUID = UUIDField(pk=True)
    created_at: datetime = DatetimeField(auto_now_add=True)
    modified_at: datetime = DatetimeField(auto_now=True)

    class Meta:
        """TODO generate docstring"""

        abstract = True

    @classmethod
    async def get_all(cls: Type[_MODEL], lock=True) -> list[_MODEL]:
        """TODO generate docstring"""
        if lock:
            return await cls.all().select_for_update()
        return await cls.all()

    @classmethod
    async def get_by_id(cls: Type[_MODEL], model_id: UUID, lock=True) -> _MODEL:
        """TODO generate docstring"""
        if lock:
            return await cls.select_for_update().get(id=model_id)
        return await cls.get(id=model_id)

    @classmethod
    async def get_latest(cls: Type[_MODEL], lock=True) -> _MODEL | None:
        """TODO generate docstring"""
        if lock:
            return await cls.select_for_update().order_by("-created_at").first()
        return await cls.all().order_by("-created_at").first()

    @classmethod
    async def get_latest_amount(
        cls: Type[_MODEL], amount: int, offset: int, order: str = "-created_at", lock=False
    ) -> list[_MODEL]:
        """TODO generate docstring"""
        if lock:
            return await cls.all().select_for_update().order_by(order).offset(offset).limit(amount)
        return await cls.all().order_by(order).offset(offset).limit(amount)

    @classmethod
    def __sacl__(cls) -> list[AclEntry] | None:
        return None

    async def __dacl__(self) -> list[list[AclEntry]] | None:
        return None
