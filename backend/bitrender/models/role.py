"""Contains a database model describing user roles."""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Type, TypeVar, Union

from tortoise.fields import BooleanField, ReverseRelation, TextField
from tortoise.queryset import QuerySetSingle

from bitrender.core.acl import AclEntry, StaticAclEntries
from bitrender.models.base import BaseModel
from bitrender.schemas import RoleView

if TYPE_CHECKING:
    from bitrender.models import RolePermission, User


MODEL = TypeVar("MODEL", bound="Role")


class Role(BaseModel):
    """Model that defines a user's role in the system. Each role has assigned a set of permissions.


    Attributes:
        name (str): The name of the role.
        permissions (ReverseRelation[RolePermission]): A reverse relation, with the permission\
             entries of the role.
        users (ReverseRelation[User]): A reverse relation, with the users\
             that have the role assigned.
        default (bool | None): Defines, if this is the default role that is used when registering\
             new users."""

    name: str = TextField()

    permissions: ReverseRelation[RolePermission]
    users: ReverseRelation[User]

    default: bool | None = BooleanField(default=None, null=True, unique=True)  # type: ignore

    columns = Literal["id", "created_at", "modified_at", "name", "default"]

    @classmethod
    def get_default(cls: Type[MODEL], lock: bool = True) -> QuerySetSingle[MODEL]:
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
            return cls.get(default=True)
        return cls.select_for_update().get(default=True)

    @property
    async def acl_id_list(self) -> list[str]:
        """Returns authentication identifiers from it's permissions.

        Returns:
            list[str]: List of authentication identifiers."""
        return [permission.acl_id for permission in await self.permissions]

    async def to_view(self) -> RoleView:
        """Converts the role model to RoleView schema

        Returns:
            RoleView: View used by the app to display roles permissions and other data"""
        return RoleView(
            id=self.id,
            created_at=self.created_at,
            modified_at=self.modified_at,
            name=self.name,
            default=self.default,
            permissions=[role_permission.permission for role_permission in await self.permissions],
        )

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_SUPERUSER, StaticAclEntries.IS_AUTHENTICATED]

    async def __dacl__(self) -> list[list[AclEntry]]:
        acl: list[list[AclEntry]] = [[StaticAclEntries.DENY_EVERYONE]]
        await self.extend_dacl(self.permissions, acl)
        return acl
