"""Contains all errors related to authenticating and authorizing users."""
from bitrender.errors import AppError


class UserError(AppError):
    """Base error for all errors related to authenticating and authorizing users."""


class UnauthorizedError(UserError):
    """Raised if the entity requesting a resource has no access to it"""


class UnauthenticatedError(UserError):
    """Raised, when there is no entity authenticated when accessing a resource"""


class CredentialsError(UserError):
    """Raised, when the provided credentials were wrong."""


class UserNotVerified(UserError):
    """Raised when the user is not verified"""


class UserNotActive(UserError):
    """Raised when the user is not active"""
