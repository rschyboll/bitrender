from bitrender.errors import AppError


class AuthError(AppError):
    pass


class UnauthorizedError(AuthError):
    """Raised if the entity requesting a resource has no access to it"""

    code = "NOT_AUTHORIZED"


class UnauthenticatedError(AuthError):
    """Raised, when there is no entity authenticated when accessing a resource"""

    code = "NOT_AUTHENTICATED"


class TokenCorruptedError(AuthError):
    """Raised when the received auth token got corrupted"""


class TokenExpiredError(AuthError):
    """Raised when the received auth token is expired"""
