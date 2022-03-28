"""This module contains dependencies for user authorization."""
from datetime import datetime, timedelta
from enum import Enum

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from bitrender.models import User

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AclAction(Enum):
    """TODO generate docstring"""

    CREATE = "create"
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class AclPermit(Enum):
    """TODO generate docstring"""

    ALLOW = "Allow"
    DENY = "Deny"


AclEntry = tuple[AclPermit, str, AclAction]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> bytes:
    """TODO generate docstring"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


def check_password(password: str, password_hash: bytes) -> bool:
    """TODO generate docstring"""

    return bcrypt.checkpw(password.encode(), password_hash)


def create_access_token(data: dict) -> str:
    """TODO generate docstring"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """TODO generate docstring"""

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
