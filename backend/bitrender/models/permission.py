"""This module contains classes/database models describing user permissions."""
from enum import Enum, unique
from typing import TYPE_CHECKING

from tortoise.fields import CharEnumField, ForeignKeyField, ForeignKeyRelation

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role
else:
    Role = object


@unique
class PermissionStr(Enum):
    """Static enum containing available user permissions."""

    READ_TASK = "read_task"
    CREATE_TASK = "create_task"
    DELETE_TASK = "delete_task"
    MANAGE_TASKS = "manage_tasks"

    CREATE_ROLE = "create_role"
    UPDATE_ROLE = "update_role"
    DELETE_ROLE = "delete_role"


class Permission(BaseModel):
    """Database model describing permissions assigned to a specific user role.

    Attributes:
        name (PermissionsEnum): Permission name.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned."""

    name = CharEnumField(PermissionStr, max_length=32)
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    @property
    def auth_id(self) -> str:
        """Returns authentication identifier of the permission.

        Returns:
            str: Auth id."""
        return f"permission:{self.name}"
