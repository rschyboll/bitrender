"""TODO create docstring"""
from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

from tortoise.fields import (
    BinaryField,
    BooleanField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
)

from bitrender.core.acl import (
    AUTHENTICATED,
    EVERYONE,
    AclAction,
    AclEntry,
    AclPermit,
    StaticAclEntries,
)
from bitrender.models import Permission
from bitrender.models.base import BaseModel
from bitrender.schemas import UserView

if TYPE_CHECKING:
    from bitrender.models import Role

MODEL = TypeVar("MODEL", bound="User")


class User(BaseModel):
    """TODO create docstring"""

    email: str = CharField(255, unique=True)
    hashed_password: bytes = BinaryField()

    verify_token: str | None = CharField(255, null=True)
    reset_password_token: str | None = CharField(255, null=True)

    is_active: bool = BooleanField(default=True)  # type: ignore
    is_superuser: bool = BooleanField(default=False)  # type: ignore
    is_verified: bool = BooleanField(default=False)  # type: ignore

    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    @classmethod
    async def get_by_username(cls: Type[MODEL], username: str, lock=True) -> MODEL:
        """Returns a user based on the provided username.

        Args:
            username (str): Username of the user that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.

        Raises:
            DoesNotExist: Raised if no user with the provided username exists.

        Returns:
            MODEL: User entry selected from the database."""
        if not lock:
            return await cls.get(username=username)
        return await cls.select_for_update().get(username=username)

    @classmethod
    async def get_by_email(cls: Type[MODEL], email: str, lock=True) -> MODEL:
        """Returns a user based on the provided email.

        Args:
            email (str): Email of the user that should be selected.
            lock (bool, optional): Specifies if the entry should be locked, \
                adds FOR UPDATE to the query. Defaults to True.

        Raises:
            DoesNotExist: Raised if no user with the provided email exists.

        Returns:
            MODEL: User entry selected from the database."""
        if not lock:
            return await cls.get(email=email)
        return await cls.select_for_update().get(email=email)

    @property
    async def acl_id_list(self) -> list[str]:
        """TODO create docstring"""
        role = await self.role
        return [self.acl_id, *(await role.acl_id_list)]

    @property
    def acl_id(self) -> str:
        """TODO create docstring"""
        return f"user:{self.id}"

    async def to_view(self) -> UserView:
        """Converts the user model to pydantic UserView.

        Returns:
            UserView: View used by frontend to display user data."""
        role = await self.role
        permissions = [role_permission.permission for role_permission in (await role.permissions)]
        return UserView(
            id=self.id,
            created_at=self.created_at,
            modified_at=self.modified_at,
            email=self.email,
            role=role.name,
            permissions=permissions,
        )

    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [
            StaticAclEntries.IS_SUPERUSER,
            (
                AclPermit.NOTDENY,
                AUTHENTICATED,
                [AclAction.VIEW, AclAction.EDIT, AclAction.DELETE],
            ),
            (
                AclPermit.ALLOW,
                Permission.MANAGE_USERS.acl_id,
                [AclAction.CREATE, AclAction.VIEW, AclAction.EDIT, AclAction.DELETE],
            ),
        ]

    async def __dacl__(self) -> list[list[AclEntry]]:
        acl: list[list[AclEntry]] = [[(AclPermit.ALLOW, self.acl_id, AclAction.VIEW)]]
        await self.extend_dacl(self.role, acl)
        if (await self.role).default:
            acl[0].insert(0, (AclPermit.DENY, AUTHENTICATED, AclAction.CREATE))
            acl[0].append((AclPermit.ALLOW, EVERYONE, AclAction.CREATE))
        return acl
