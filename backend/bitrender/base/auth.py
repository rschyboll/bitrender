"""This module contains dependencies for user authorization."""
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from bitrender.models import Permissions, User
from bitrender.schemas import TokenData

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """TODO generate docstring."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError) as error:
        raise credentials_exception from error
    user = await User.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


class HasPermission:
    """TODO generate docstring"""

    def __init__(self, permissions: list[Permissions]):
        self.permissions = permissions

    def __call__(self):
        pass
