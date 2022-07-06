"""Contains error handlers for errors raised from services."""

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from bitrender.errors.user import (
    BadCredentials,
    NoDefaultRole,
    UnauthenticatedError,
    UnauthorizedError,
    UserAlreadyExists,
    UserNotVerified,
)

error_codes = {
    # Global system errors
    DoesNotExist: "RESOURCE_NOT_FOUND",
    # User errors
    UnauthenticatedError: "NOT_AUTHENTICATED",
    UnauthorizedError: "NOT_AUTHORIZED",
    UserNotVerified: "USER_NOT_VERIFIED",
    BadCredentials: "BAD_CREDENTIALS",
    UserAlreadyExists: "USER_ALREADY_EXISTS",
    NoDefaultRole: "NO_DEFAULT_ROLE",
}


def register_library_error_handlers(app: FastAPI) -> None:
    """Registers all library error handlers."""
    app.add_exception_handler(DoesNotExist, does_not_exist_handler)


def does_not_exist_handler(_: Response, __: DoesNotExist) -> JSONResponse:
    """Error handler for DoesNotExist"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": error_codes[DoesNotExist]},
    )
