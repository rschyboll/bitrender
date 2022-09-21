"""TODO generate docstring"""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from bitrender.auth.acl import AclAction
from bitrender.errors.user import RoleDoesNotExist, UserAlreadyExists
from bitrender.models import Role, User
from bitrender.schemas.user import UserCreate
from bitrender.services.auth import PasswordHelperProtocol

if TYPE_CHECKING:
    from bitrender.services import Services


class UserService:
    """TODO generate docstring"""

    def __init__(self, services: Services, password_helper: PasswordHelperProtocol):
        self.services = services
        self.password = password_helper

    async def create(self, user_data: UserCreate, role: Role | UUID) -> User:
        """TODO generate docstring"""
        hashed_password = self.password.hash(user_data.password.get_secret_value())
        if await User.exists(email=user_data.email):
            raise UserAlreadyExists()
        if isinstance(role, UUID):
            try:
                role = await Role.get_by_id(role)
            except DoesNotExist as error:
                raise RoleDoesNotExist() from error
        return await self.services.auth.action(
            User.create,
            AclAction.CREATE,
            {**user_data.dict(), "role": role, "hashed_password": hashed_password},
        )
