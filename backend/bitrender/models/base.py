"""Contains the base class for all database models."""
from __future__ import annotations

from datetime import datetime
from typing import Type, TypeVar
from uuid import UUID

from tortoise.fields import (
    DatetimeField,
    ForeignKeyRelation,
    OneToOneNullableRelation,
    ReverseRelation,
    UUIDField,
)
from tortoise.models import Model

from bitrender.auth.acl import EVERYONE, AclAction, AclEntry, AclList, AclPermit

MODEL = TypeVar("MODEL", bound="BaseModel")


class BaseModel(Model):
    """Class that serves as the base for all database models.

    Attributes:
        id (UUID): Primary key of the database entry.
        created_at (datetime): Datetime, when the entry was created.
        modified_at (datetime): Datetime, when the entry was modified."""

    id: UUID = UUIDField(pk=True)
    created_at: datetime = DatetimeField(auto_now_add=True)
    modified_at: datetime = DatetimeField(auto_now=True)

    class Meta:
        """BaseModel config."""

        abstract = True

    @classmethod
    async def get_all(cls: Type[MODEL], lock=True, skip_locked=False) -> list[MODEL]:
        """Returns all database entries of the given model.

        Args:
            lock (bool, optional): Specifies if the entries should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
            skip_locked (bool, optional): Specifies if the query should skip all rows that are \
                currently locked. Defaults to False.
        Returns:
            List[_MODEL]: List of entries extracted from the database"""
        if not lock:
            return await cls.all()
        return await cls.all().select_for_update(skip_locked=skip_locked)

    @classmethod
    async def get_by_id(cls: Type[MODEL], model_id: UUID, lock=True) -> MODEL:
        """Returns a database entry based on the provided id.

        Args:
            model_id (UUID): Id of the database entry that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
        Returns:
            _MODEL: Entry of the model extracted from the database."""
        if not lock:
            return await cls.get(id=model_id)
        return await cls.select_for_update().get(id=model_id)

    @classmethod
    async def get_latest(cls: Type[MODEL], lock=True) -> MODEL | None:
        """Returns the last created database entry of the model.

        Args:
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
        Returns:
            _MODEL: Entry of the model extracted from the database."""
        if not lock:
            return await cls.all().order_by("-created_at").first()
        return await cls.select_for_update().order_by("-created_at").first()

    @classmethod
    async def get_amount(
        cls: Type[MODEL],
        amount: int,
        offset: int,
        order: str = "-created_at",
        lock=True,
        skip_locked=False,
    ) -> list[MODEL]:
        """Returns a specified amount of database entries of the model.

        Args:
            amount (int): Amount of entries to select.
            offset (int): First entry to select from.
            order (str, optional): How to order the results. Defaults to "-created_at".
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.
            skip_locked (bool, optional): Specifies if the query should skip all rows that are \
                currently locked. Defaults to False.

        Returns:
            list[_MODEL]: Selected database entries."""
        if not lock:
            return await cls.all().order_by(order).offset(offset).limit(amount)
        return (
            await cls.all()
            .select_for_update(skip_locked=skip_locked)
            .order_by(order)
            .offset(offset)
            .limit(amount)
        )

    @staticmethod
    async def extend_dacl(
        relation: ForeignKeyRelation[MODEL]
        | OneToOneNullableRelation[MODEL]
        | ReverseRelation[MODEL],
        acl: list[list[AclEntry]],
    ) -> list[list[AclEntry]]:
        """TODO generate docstring"""
        if isinstance(relation, BaseModel):
            relation_acl = await relation.__dacl__()
            acl.extend(relation_acl)
        elif isinstance(relation, ReverseRelation) and relation._fetched:  # pylint: disable=W0212
            for item in relation:
                relation_item_acl = await item.__dacl__()
                acl.extend(relation_item_acl)
        return acl

    @classmethod
    def __sacl__(cls) -> AclList:
        return [(AclPermit.DENY, EVERYONE, AclAction.VIEW)]

    async def __dacl__(self) -> list[AclList]:
        return [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
