"""TODO generate docstring"""


from datetime import datetime, timedelta
from typing import Protocol
from uuid import UUID

from jose import jwt
from pydantic import BaseModel as PydanticBase

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(PydanticBase):
    """Class containing data decoded from JWT.

    Attributes:
        id (UUID) - User id"""

    sub: UUID
    exp: int


class TokenHelperProtocol(Protocol):
    """TODO generate docstring"""

    def create_token(self, user_id: UUID) -> str:
        """TODO generate docstring"""

    def decode_token(self, token: str) -> TokenData:
        """TODO generate docstring"""


class TokenHelper:
    """TODO generate docstring"""

    @staticmethod
    def create_token(user_id: UUID) -> str:
        """Creates a JWT token with the given data.

        Args:
            user_id (UUID): Id of the user

        Returns:
            str: Created JWT"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expire, "sub": user_id.hex}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> TokenData:
        """Decodes the JWT doken and returns data that was contained with it.

        Args:
            token (str): JWT that should be decoded.

        Returns:
            TokenData: Data that was contained within the JWT"""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
