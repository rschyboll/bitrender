"""This module contains classes/database models describing user permissions."""
from enum import IntEnum
from typing import TYPE_CHECKING

from tortoise.fields import BooleanField, ForeignKeyField, ForeignKeyRelation, IntEnumField

from bitrender.models.base import BaseModel
from bitrender.schemas.permission import RoleHasPermissionView

if TYPE_CHECKING:
    from bitrender.models import Role
else:
    Role = object


class Permission(IntEnum):
    """Static enum containing available user permissions."""

    READ_TASK = 1
    CREATE_TASK = 2
    DELETE_TASK = 3
    BROWSE_TASKS = 4

    BROWSE_ROLES = 100
    CREATE_ROLE = 101
    UPDATE_ROLE = 102
    DELETE_ROLE = 103


class RoleHasPermission(BaseModel[RoleHasPermissionView]):
    """Database model describing permissions assigned to a specific user role.


    Attributes:
        permission (Permission): Permission that is beeing assigned.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned.
        initial (bool): If the permission is an initial system permission and cannot be deleted."""

    def __init__(self, permission: Permission, role: Role, **kwargs):
        super().__init__(permission=permission, role=role, **kwargs)

    permission: Permission = IntEnumField(Permission)

    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> RoleHasPermissionView:
        """Converts the model to it's corresponding pydantic schema."""
        return RoleHasPermissionView.from_orm(self)
