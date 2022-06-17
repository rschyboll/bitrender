from fastapi import Request

from bitrender.errors import AppError


class AuthError(AppError):
    pass


class UnauthorizedError(AuthError):
    """Raised if the entity requesting a resource has no access to it"""


async def unauthorized_error_handler(request: Request, error: UnauthorizedError):
    pass


class UnauthenticatedError(AuthError):
    """Raised, when there is no entity authenticated when accessing a resource"""


class TokenCorruptedError(AuthError):
    """Raised when the received auth token got corrupted"""


class TokenExpiredError(AuthError):
    """Raised when the received auth token is expired"""


def add_exception_handlers():
    pass
