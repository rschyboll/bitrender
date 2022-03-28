"""This module contains a database models describing user roles."""
from typing import TYPE_CHECKING

from tortoise.fields import ReverseRelation, TextField

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Permission
else:
    Permission = object


class Role(BaseModel):
    """TODO generate docstring"""

    name: str = TextField()
    permissions: ReverseRelation[Permission]

    @property
    async def auth_ids(self) -> list[str]:
        """Returns authentication identifiers from it's permissions.

        Returns:
            list[str]: List of authentication identifiers."""
        return [permission.auth_id for permission in await self.permissions]
