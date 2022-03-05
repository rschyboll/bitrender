"""This module contains a database model describing user roles."""

from typing import TYPE_CHECKING

from tortoise.fields import BooleanField, ReverseRelation, TextField

from bitrender.models import BaseModel
from bitrender.schemas import RoleView

if TYPE_CHECKING:
    from bitrender.models import RoleHasPermission
else:
    RoleHasPermission = object


class Role(BaseModel[RoleView]):
    """Database model describing a user role.

    Attributes:
        permission (Permission): Permission that is beeing assigned.
        role (ForeignKeyRelation[Role]): Role, to which the permission is beeing assigned.
        initial (bool): If the permission is an initial system permission and cannot be deleted."""

    name: str = TextField()
    permissions: ReverseRelation[RoleHasPermission]

    initial: bool = BooleanField()  # type: ignore

    def to_view(self) -> RoleView:
        """Converts the model to it's corresponding pydantic schema."""
        return RoleView.from_orm(self)
