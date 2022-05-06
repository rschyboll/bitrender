"""TODO generate docstring"""
from typing import Protocol
from uuid import UUID

from bitrender.auth.jwt import TokenData
from bitrender.services import Services


class PasswordHelperProtocol(Protocol):
    """TODO generate docstring"""

    def hash(self, password: str) -> bytes:
        """TODO generate docstring"""

    def verify(self, password: str, hashed_password: bytes) -> bool:
        """TODO generate docstring"""


class TokenHelperProtocol(Protocol):
    """TODO generate docstring"""

    def create_token(self, user_id: UUID) -> str:
        """TODO generate docstring"""

    def decode_token(self, token: str) -> TokenData:
        """TODO generate docstring"""

class AclHelperProtocol(Protocol):
    """TODO generate docstring"""

    def query()

class AclHelperProtocol(Protocol):
    pass


class AuthService:
    """TODO generate docstring"""

    def __init__(
        self,
        services: Services,
        auth_ids: list[str],
        password_helper: PasswordHelperProtocol,
        token_helper: TokenHelperProtocol,
    ):
        self.services = services
        self.auth_ids = auth_ids
        self.password = password_helper
        self.token = token_helper

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> str:
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
