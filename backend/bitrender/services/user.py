from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from bitrender.auth.jwt import create_token
from bitrender.auth.password import hash_password, verify_password
from bitrender.errors.user import (
    BadCredentials,
    NoDefaultRole,
    RoleDoesNotExist,
    UserAlreadyExist,
    UserNotVerified,
)
from bitrender.models import Role, User
from bitrender.schemas.user import UserCreate


async def register(user_data: UserCreate) -> User:
    try:
        role = await Role.get_default(False)
    except DoesNotExist as error:
        raise NoDefaultRole() from error
    return await create(user_data, role)


async def create(user_data: UserCreate, role: Role | UUID) -> User:
    hashed_password = hash_password(user_data.password.get_secret_value())
    if await User.exists(email=user_data.email):
        raise UserAlreadyExist()
    if isinstance(role, UUID):
        try:
            role = await Role.get_by_id(role)
        except DoesNotExist as error:
            raise RoleDoesNotExist() from error
    return await User.create(**user_data.dict(), role=role, hashed_password=hashed_password)


async def authenticate(credentials: OAuth2PasswordRequestForm) -> str | None:
    try:
        user = await User.get_by_email(credentials.username)
    except DoesNotExist as error:
        raise BadCredentials() from error
    if not verify_password(credentials.password, user.hashed_password):
        raise BadCredentials()
    if not user.is_verified:
        raise UserNotVerified()
    if not user.is_active:
        raise BadCredentials()
    return create_token(user.id)
