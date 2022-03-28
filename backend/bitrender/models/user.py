"""TODO create docstring"""
from typing import TYPE_CHECKING

from tortoise.fields import (
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneField,
    OneToOneNullableRelation,
)

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role, UserAuth
else:
    UserAuth = object
    Role = object


class User(BaseModel):
    """TODO create docstring"""

    username: str = CharField(32, unique=True)
    email: str = CharField(255, unique=True)

    auth: OneToOneNullableRelation[UserAuth] = OneToOneField(
        "bitrender.UserAuth", null=True, default=None
    )
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    @property
    async def auth_ids(self) -> list[str]:
        """TODO create docstring"""
        role = await self.role
        permissions = await role.permissions
        return [self.auth_id, *[permission.name.value for permission in permissions]]

    @property
    def auth_id(self) -> str:
        """TODO create docstring"""
