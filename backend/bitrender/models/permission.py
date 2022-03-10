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


class Permissions(IntEnum):
    """Static enum containing available user permissions."""

    READ_TASKS = 1
    ADD_TASKS = 2
    REMOVE_TASKS = 3


class RoleHasPermission(BaseModel[RoleHasPermissionView]):
    """Database model describing permissions assigned to a specific user role.


    Attributes:
        permission (Permission): Permission that is beeing assigned.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned.
        initial (bool): If the permission is an initial system permission and cannot be deleted."""

    def __init__(self, permission: Permissions, role: Role, **kwargs):
        super().__init__(permission=permission, role=role, **kwargs)

    permission: Permissions = IntEnumField(Permissions)

    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> RoleHasPermissionView:
        """Converts the model to it's corresponding pydantic schema."""
        return RoleHasPermissionView.from_orm(self)
