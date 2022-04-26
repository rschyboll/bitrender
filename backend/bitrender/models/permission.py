"""Contains classes/database models describing user permissions."""
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING

from tortoise.fields import CharEnumField, ForeignKeyField, ForeignKeyRelation

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role


@unique
class Permission(Enum):
    """Static enum containing available user permissions."""

    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"

    @property
    def acl_id(self):
        """TODO generate docstring"""
        return f"permission:{self.value}"

    @classmethod
    def list(cls):
        """TODO generate docstring"""
        return list(Permission)


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
