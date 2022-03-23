"""This module contains classes/database models describing user permissions."""
from enum import Flag, auto

from tortoise.fields import BooleanField, ForeignKeyField, ForeignKeyRelation, IntEnumField

from bitrender import models


class Permission(Flag):
    """Static enum containing available user permissions."""

    READ_TASK = auto()
    CREATE_TASK = auto()
    DELETE_TASK = auto()
    MANAGE_TASKS = auto()

    CREATE_ROLE = auto()
    UPDATE_ROLE = auto()
    DELETE_ROLE = auto()



class RoleHasPermissionView(models.BaseView):
    permission: Permission
    role: models.RoleView
    removable: bool


class RoleHasPermission(models.BaseModel[RoleHasPermissionView]):
    """Database model describing permissions assigned to a specific user role.


    Attributes:
        permission (Permission): Permission that is beeing assigned.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned.
        initial (bool): If the permission is an initial system permission and cannot be deleted."""

    permission: Permission = IntEnumField(Permission)

    role: ForeignKeyRelation[models.Role] = ForeignKeyField("bitrender.Role")

    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> RoleHasPermissionView:
        """Converts the model to it's corresponding pydantic schema."""
        return RoleHasPermissionView.from_orm(self)
