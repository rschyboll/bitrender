"""This module contains a database models describing user roles."""

from tortoise.fields import BooleanField, ReverseRelation, TextField

from bitrender import models


class RoleView(models.BaseView):
    """TODO generate docstring"""

    name: str
    permissions: list[models.RoleHasPermissionView]
    removable: bool


class Role(models.BaseModel[RoleView]):
    """TODO generate docstring"""

    name: str = TextField()
    permissions: ReverseRelation[models.RoleHasPermission]
    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> RoleView:
        """Converts the model to it's corresponding pydantic schema."""
        return RoleView.from_orm(self)


# TODO Zamienić modele pydantic tak żeby miały tylko relacje w jedną stronę
