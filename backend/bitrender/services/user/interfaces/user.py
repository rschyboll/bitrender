"""TODO generate docstring"""
from abc import abstractmethod
from uuid import UUID

from antidote import interface

from bitrender.schemas import UserCreate, UserView


@interface
class IUserService:
    """TODO generate docstring"""

    @abstractmethod
    async def get_current(self) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> str:
        """Tries to authenticate a user with the given credentials,
            and creates a web token with the user id when the authentication was successful.

        Args:
            email (str): _description_
            password (str): _description_

        Raises:
            CredentialsError: Could not authenticate a user with those credentials.
            UserNotVerified: User that was beeing authenticated is not verified.
            UserNotActive: User that was beeing authenticated is not active.

        Returns:
            str: Token containing the authentiated users data."""

    @abstractmethod
    async def register(self, user_data: UserCreate) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def create(self, user_data: UserCreate, role: UUID) -> UserView:
        """TODO generate docstring"""
