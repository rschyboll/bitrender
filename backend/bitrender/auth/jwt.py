"""Contains logic for creating and decoding JWTs."""


from datetime import datetime, timedelta
from uuid import UUID

from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import BaseModel as PydanticBase

from bitrender.errors.auth import TokenCorruptedError, TokenExpiredError

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(PydanticBase):
    """Class containing data decoded from JWT.

    Attributes:
        sub (UUID) - User id
        exp (int) - Expiration time of the token"""

    sub: UUID
    exp: int


class TokenHelper:
    """Class with helper methods for JWTs."""

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

        Raises:
            TokenExpiredError: Raised when the token has expired.
            TokenCorruptedError: Raised when could not decode the token.

        Returns:
            TokenData: Data that was contained within the JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return TokenData(**payload)
        except ExpiredSignatureError as error:
            raise TokenExpiredError() from error
        except JWTError as error:
            raise TokenCorruptedError() from error
