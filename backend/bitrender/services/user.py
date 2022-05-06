from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from bitrender.auth.deps import AuthService
from bitrender.auth.jwt import create_token
from bitrender.auth.password import hash_password, verify_password
from bitrender.errors.auth import BadCredentialsError
from bitrender.errors.user import (
    BadCredentialsError,
    NoDefaultRoleException,
    RoleDoesNotExist,
    UserAlreadyExist,
    UserNotVerifiedError,
)
from bitrender.models import Role, User
from bitrender.schemas.user import UserCreate
from bitrender.services import Services


class UserService:
    def __init__(self, services: Services):
        self.services = services

    async def register(self, user_data: UserCreate) -> User:
        try:
            role = await Role.get_default(False)
        except DoesNotExist as error:
            raise NoDefaultRoleException() from error
        return await self.create(user_data, role)

    async def create(self, user_data: UserCreate, role: Role | UUID) -> User:
        hashed_password = hash_password(user_data.password.get_secret_value())
        if await User.exists(email=user_data.email):
            raise UserAlreadyExist()
        if isinstance(role, UUID):
            try:
                role = await Role.get_by_id(role)
            except DoesNotExist as error:
                raise RoleDoesNotExist() from error
        return await User.create(**user_data.dict(), role=role, hashed_password=hashed_password)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> str | None:
        try:
            user = await User.get_by_email(credentials.username)
        except DoesNotExist as error:
            raise BadCredentialsError() from error
        if not verify_password(credentials.password, user.hashed_password):
            raise BadCredentialsError()
        if not user.is_verified:
            raise UserNotVerifiedError()
        if not user.is_active:
            raise BadCredentialsError()
        return create_token(user.id)
