"""Contains error handlers for authentication and authorization errors"""
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

from bitrender.api.handlers import error_codes
from bitrender.errors.user import (
    BadCredentials,
    EmailTaken,
    NoDefaultRole,
    UnauthenticatedError,
    UnauthorizedError,
    UsernameTaken,
    UserNotVerified,
)


def register_user_error_handlers(app: FastAPI) -> None:
    """Registers all user error handlers"""
    app.add_exception_handler(UnauthenticatedError, unauthenticated_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(UserNotVerified, user_not_verified_handler)
    app.add_exception_handler(BadCredentials, credentials_error_handler)
    app.add_exception_handler(UsernameTaken, username_taken_handler)
    app.add_exception_handler(EmailTaken, email_taken_handler)
    app.add_exception_handler(NoDefaultRole, no_default_role_handler)


async def unauthenticated_error_handler(_: Response, __: UnauthenticatedError) -> JSONResponse:
    """Error handler for UnauthenticatedError"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[UnauthenticatedError]},
    )


async def unauthorized_error_handler(_: Response, __: UnauthorizedError) -> JSONResponse:
    """Error handler for UnauthorizedError"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[UnauthorizedError]},
    )


async def user_not_verified_handler(_: Response, __: UserNotVerified) -> JSONResponse:
    """Error handler for UserNotVerified"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[UserNotVerified]},
    )


async def credentials_error_handler(_: Response, __: BadCredentials) -> JSONResponse:
    """Error handler for UserNotActive"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[BadCredentials]},
    )


async def username_taken_handler(_: Response, __: UsernameTaken) -> JSONResponse:
    """Error handler for UserAlreadyExists"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": error_codes[UsernameTaken]},
    )


async def email_taken_handler(_: Response, __: EmailTaken) -> JSONResponse:
    """Error handler for UserAlreadyExists"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": error_codes[EmailTaken]},
    )


async def no_default_role_handler(_: Response, __: NoDefaultRole) -> JSONResponse:
    """Error handler for NoDefaultRole"""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": error_codes[NoDefaultRole]},
    )
