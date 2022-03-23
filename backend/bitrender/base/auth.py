"""This module contains dependencies for user authorization."""
import functools
from datetime import datetime, timedelta
from typing import Callable, Container, ParamSpec, TypeVar

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from bitrender.models import Permission, User
from bitrender.schemas import TokenData

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> bytes:
    """Hashes password using the bcrypt algorithm.

    Args:
        password (str): Plain string password to hash.

    Returns:
        bytes: Hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


def check_password(password: str, password_hash: bytes) -> bool:
    """Checks password against a hashed password.

    Args:
        password (str): Plain string password that is checked.
        hashed_password (bytes): Hashed password.

    Returns:
        bool: If the password is correct."""
    return bcrypt.checkpw(password.encode(), password_hash)


def create_access_token(data: dict) -> str:
    """Creates a JWT with the passed data.

    Args:
        data (dict): Dict containing data that should be included in the JWT.

    Returns:
        str: JWT containing signed data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """Decodes a JWT and parses it to TokenData form.

    Args:
        token (str): JWT to decode.

    Returns:
        TokenData: Data present in the JWT."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return TokenData(**payload)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """TODO generate docstring."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError) as error:
        raise credentials_exception from error
    user = await User.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


class UserWithPermissions:
    """TODO generate docstring"""

    def __init__(self, *permissions: list[Permission]):
        self.permissions = permissions

    async def __call__(self, user: User = Depends(get_current_user)) -> User:
        role = await user.role
        user_permissions = [has_permission.permission for has_permission in await role.permissions]
        for permission in self.permissions:
            if permission not in user_permissions:
                raise credentials_exception
        return user


T = TypeVar("T")
P = ParamSpec("P")


def testt():
    def my_decorator(func: Callable[P, T]) -> Callable[P, Container[T]]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return my_decorator


@testt()
async def test(i: int, s: str):
    pass


test()
