"""Contains error handlers for errors raised from services."""

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from bitrender.errors.user import UnauthenticatedError, UnauthorizedError, UserNotVerified


def register_library_error_handlers(app: FastAPI):
    """Registers all library error handlers."""
    app.add_exception_handler(DoesNotExist, does_not_exist_handler)


def does_not_exist_handler(_: Response, __: DoesNotExist):
    """Error handler for DoesNotExist"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": error_codes[DoesNotExist]},
    )
