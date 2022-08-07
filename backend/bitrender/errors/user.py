"""Contains all errors related to authenticating and authorizing users."""
from bitrender.errors import AppError


class UserError(AppError):
    """Base error for all errors related to authenticating and authorizing users."""


class UnauthorizedError(UserError):
    """Raised if the entity requesting a resource has no access to it"""


class UnauthenticatedError(UserError):
    """Raised, when there is no entity authenticated when accessing a resource"""


class BadCredentials(UserError):
    """Raised, when the provided credentials were wrong."""


class UserNotVerified(UserError):
    """Raised when the user is not verified"""


class UsernameTaken(UserError):
    """Raised when creating user, and a user with the name already exists."""


class EmailTaken(UserError):
    """Raised when creating user, and a user with the email already exists."""


class NoDefaultRole(UserError):
    """Raised when creating user, and no default role is selected"""


class RoleDoesNotExist(UserError):
    """Raised when creating user, and the selected role for the new user does not exist"""
