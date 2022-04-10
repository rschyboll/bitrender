"""TODO create docstring"""
from typing import TYPE_CHECKING

from tortoise.fields import (
    BooleanField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneField,
    OneToOneNullableRelation,
)

from bitrender.base.auth import AclAction, AclEntry, AclPermit, StaticAclEntries
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

    active: bool = BooleanField()  # type: ignore

    auth: OneToOneNullableRelation[UserAuth] = OneToOneField("bitrender.UserAuth")
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
        return f"user:{self.id}"

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [StaticAclEntries.IS_AUTHENTICATED]

    async def __dacl__(self) -> list[list[AclEntry]]:
        return [[(AclPermit.ALLOW, self.auth_id, AclAction.VIEW)]]
