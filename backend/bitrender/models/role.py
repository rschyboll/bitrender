"""Contains a database model describing user roles."""
from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from tortoise.fields import BooleanField, ReverseRelation, TextField

from bitrender.base.acl import AclEntry, StaticAclEntries
from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import RolePermission, User


MODEL = TypeVar("MODEL", bound="Role")


class Role(BaseModel):
    """TODO generate docstring"""

    name: str = TextField()

    permissions: ReverseRelation[RolePermission]
    users: ReverseRelation[User]

    default: bool | None = BooleanField(default=None, null=True, unique=True)  # type: ignore

    @classmethod
    async def get_default(cls: Type[MODEL], lock=True) -> MODEL:
        """Returns the current default role.

        Args:
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.

        Raises:
            DoesNotExist: Raised if no default role exists.
            MultipleObjectsReturned: Raised it they are many default roles, which indicates a bug.

        Returns:
            MODEL: The default role."""
        if not lock:
            return await cls.get(default=True)
        return await cls.select_for_update().get(default=True)

    @property
    async def acl_id_list(self) -> list[str]:
        """Returns authentication identifiers from it's permissions.

        Returns:
            list[str]: List of authentication identifiers."""
        return [permission.acl_id for permission in await self.permissions]

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_AUTHENTICATED]
