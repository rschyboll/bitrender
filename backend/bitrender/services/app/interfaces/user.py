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
        """Returns the current user based on the provided context.

        Required the user to have authorization to access it's own data.
        User could be not active, for example disabled by the admin, which \
        would not allow him to access his own data.

        Raises:
            UnauthenticatedError: No user present in the context.
            UnauthorizedError: User cannot read it's own data.
            UserNotVerified: User is not verified.

        Returns:
            UserView - Data of the current user"""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserView:
        """TODO generate docstring"""

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> str:
        """Tries to authenticate a user with the given credentials,\
            and creates a web token with the user id when the authentication was successful.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Raises:
            BadCredentials: Could not authenticate a user with those credentials, \
                or the user is not active.
            UserNotVerified: User that was beeing authenticated is not verified.

        Returns:
            str: Token containing the authentiated users data."""

    @abstractmethod
    async def register(self, user_data: UserCreate) -> UserView:
        """Creates a new user, with the role marked as default.

        When no default role is currently selected, it raises an error.

        Raises:
            NoDefaultRole: No default role was selected in the system.
            UserAlreadyExist: User with this credentials already exists.
            UnauthorizedError: Raised when a user is logged in, and tries to register.

        Args:
            user_data (UserCreate): Data of the new user.

        Returns:
            UserView: The created user."""

    @abstractmethod
    async def create(self, user_data: UserCreate, role: UUID) -> UserView:
        """TODO generate docstring"""
