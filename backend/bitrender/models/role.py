"""Contains a database model describing user roles."""
from typing import TYPE_CHECKING

from tortoise.fields import BooleanField, ReverseRelation, TextField

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Permission
else:
    Permission = object


class Role(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_

    Returns:
        _type_: _description_"""

    name: str = TextField()
    permissions: ReverseRelation[Permission]
    default: bool = BooleanField()  # type: ignore

    @property
    async def auth_ids(self) -> list[str]:
        """Returns authentication identifiers from it's permissions.

        Returns:
            list[str]: List of authentication identifiers."""
        return [permission.auth_id for permission in await self.permissions]
