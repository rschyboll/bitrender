"""Contains a database model describing user roles."""
from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise.fields import BooleanField, ReverseRelation, TextField

from bitrender.models.base import BaseModel
from bitrender.utils.auth import StaticAclEntries

if TYPE_CHECKING:
    from bitrender.base.auth import AclEntry
    from bitrender.models import Permission


class Role(BaseModel):
    """TODO generate docstring"""

    name: str = TextField()
    permissions: ReverseRelation[Permission]
    default: bool = BooleanField()  # type: ignore

    @property
    async def auth_ids(self) -> list[str]:
        """Returns authentication identifiers from it's permissions.

        Returns:
            list[str]: List of authentication identifiers."""
        return [permission.auth_id for permission in await self.permissions]

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_AUTHENTICATED]
