"""Contains classes/database models describing user permissions."""
from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import CharEnumField, ForeignKeyField, ForeignKeyRelation

from bitrender.core.acl import AclAction, AclEntry, AclPermit, StaticAclEntries
from bitrender.enums.permission import Permission
from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role


class RolePermission(BaseModel):
    """Database model describing permissions assigned to a specific user role.

    Attributes:
        name (PermissionsEnum): Permission name.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned."""

    permission = CharEnumField(Permission, max_length=32)
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role", related_name="permissions")

    @property
    def acl_id(self) -> str:
        """Returns authentication identifier of the permission.

        Returns:
            str: Auth id."""
        return self.permission.acl_id

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_SUPERUSER, StaticAclEntries.IS_AUTHENTICATED]

    async def __dacl__(self) -> list[list[AclEntry]]:
        acl: list[list[AclEntry]] = [[(AclPermit.ALLOW, self.acl_id, AclAction.VIEW)]]
        return acl
