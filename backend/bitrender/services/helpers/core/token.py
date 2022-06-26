"""Contains implementation for the ITokenHelper interface."""

from datetime import datetime, timedelta
from uuid import UUID

from antidote import implements, inject, wire
from jose import ExpiredSignatureError, jwt

from bitrender.config import Settings
from bitrender.errors.token import TokenCorruptedError, TokenCreateError, TokenExpiredError
from bitrender.schemas import UserTokenData
from bitrender.services.helpers.interfaces.token import ITokenHelper

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"


@wire
@implements(ITokenHelper).by_default
class TokenHelper(ITokenHelper):
    """Helper class containing implementation for creating and decrypting web tokens."""

    def create(self, data: dict, expires_delta: timedelta) -> str:
        try:
            expire = datetime.utcnow() + expires_delta
            encoded_jwt = jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
        except Exception as error:
            raise TokenCreateError() from error

    def decode(self, token: str) -> dict:
        try:
            payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except ExpiredSignatureError as error:
            raise TokenExpiredError() from error
        except Exception as error:
            raise TokenCorruptedError() from error

    def create_user_token(self, sub: UUID, settings: Settings = inject.me()) -> str:
        return self.create({"sub": sub}, timedelta(minutes=settings.user_token_expire_minutes))

    def decode_user_token(self, token: str) -> UserTokenData:
        try:
            payload = self.decode(token)
            return UserTokenData(**payload)
        except Exception as error:
            raise TokenCorruptedError() from error
