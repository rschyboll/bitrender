"""TODO create docstring"""
from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from tortoise.fields import (
    BooleanField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneField,
    OneToOneNullableRelation,
)

from bitrender.base.acl import AclAction, AclEntry, AclPermit, StaticAclEntries
from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role, UserAuth

MODEL = TypeVar("MODEL", bound="User")


class User(BaseModel):
    """TODO create docstring"""

    username: str = CharField(32, unique=True)
    email: str = CharField(255, unique=True)

    active: bool = BooleanField(default=False)  # type: ignore
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")
    auth: OneToOneNullableRelation[UserAuth] = OneToOneField(
        "bitrender.UserAuth", null=True, default=None
    )

    @classmethod
    async def get_by_username(cls: Type[MODEL], username: str, lock=True) -> MODEL:
        """Returns a user based on the provided username.

        Args:
            username (str): Username of the user that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.

        Raises:
            DoesNotExist: Raised if no user with the provided username exists.

        Returns:
            MODEL: User entry selected from the database."""
        if not lock:
            return await cls.get(username=username)
        return await cls.select_for_update().get(username=username)

    @classmethod
    async def get_by_email(cls: Type[MODEL], email: str, lock=True) -> MODEL:
        """Returns a user based on the provided email.

        Args:
            email (str): Email of the user that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.

        Raises:
            DoesNotExist: Raised if no user with the provided email exists.

        Returns:
            MODEL: User entry selected from the database."""
        if not lock:
            return await cls.get(email=email)
        return await cls.select_for_update().get(email=email)

    @property
    async def acl_id_list(self) -> list[str]:
        """TODO create docstring"""
        role = await self.role
        return [self.acl_id, *(await role.acl_id_list)]

    @property
    def acl_id(self) -> str:
        """TODO create docstring"""
        return f"user:{self.id}"

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_AUTHENTICATED]

    async def __dacl__(self) -> list[list[AclEntry]]:
        acl: list[list[AclEntry]] = [[(AclPermit.ALLOW, self.acl_id, AclAction.VIEW)]]
        await self._extend_dacl(self.role, acl)
        return acl
