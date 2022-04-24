from uuid import UUID

from tortoise.exceptions import DoesNotExist

from bitrender.auth.password import hash_password
from bitrender.models import Role, User
from bitrender.schemas.user import UserCreate


class UsersException(Exception):
    """TODO generate docstring"""


class RoleDoesNotExist(UsersException):
    """TODO generate docstring"""


class UserAlreadyExist(UsersException):
    """TODO generate docstring"""


async def register(user_data: UserCreate) -> User:
    try:
        role = await Role.get_default(False)
    except DoesNotExist as error:
        raise RoleDoesNotExist() from error
    user = await create(user_data, role)
    return user


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


async def create_jwt():
    pass
