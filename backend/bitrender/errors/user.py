"""Contains all errors related to authenticating and authorizing users."""
from bitrender.errors import AppError


class AuthError(AppError):
    """Base error for all errors related to authenticating and authorizing users."""


class UnauthorizedError(AuthError):
    """Raised if the entity requesting a resource has no access to it"""


class UnauthenticatedError(AuthError):
    """Raised, when there is no entity authenticated when accessing a resource"""


class CredentialsError(AuthError):
    """Raised, when the provided credentials were wrong."""


class TokenCorruptedError(AuthError):
    """Raised when the received auth token got corrupted"""


class TokenExpiredError(AuthError):
    """Raised when the received auth token is expired"""


class UserNotVerified(AuthError):
    """Raised when the user is not verified"""


class UserNotActive(AuthError):
    """Raised when the user is not active"""
