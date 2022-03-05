"""This module contains classes/database models describing user permissions."""
from enum import IntEnum
from typing import TYPE_CHECKING

from tortoise.fields import BooleanField, ForeignKeyField, ForeignKeyRelation, IntEnumField

from bitrender.models import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role
else:
    Role = object


class Permission(IntEnum):
    """Static enum containing available user permissions."""

    READ_TASKS = 1
    ADD_TASKS = 2
    REMOVE_TASKS = 3


class RoleHasPermission(BaseModel):
    """Database model describing permissions assigned to a specific user role.


    Attributes:
        permission (Permission): Permission that is beeing assigned.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned.
        initial (bool): If the permission is an initial system permission and cannot be deleted."""

    permission: Permission = IntEnumField(Permission)
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    initial: bool = BooleanField()  # type: ignore
