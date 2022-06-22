from abc import abstractmethod
from uuid import UUID

from antidote import interface

from bitrender.schemas import UserView

from . import IService


@interface
class IUserService(IService):
    """TODO generate docstring"""

    @abstractmethod
    async def get_current(self) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> UUID:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Raises:
            CredentialsError: Could not authenticate a user with those credentials.
            UserNotVerified: User that was beeing authenticated is not verified.
            UserNotActive: User that was beeing authenticated is not active.

        Returns:
            UUID: Id of the authenticated user+"""
        raise Exception()
