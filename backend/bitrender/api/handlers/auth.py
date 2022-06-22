"""Contains error handlers for authentication and authorization errors"""
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

from bitrender.api.handlers import error_codes
from bitrender.errors.user import UnauthenticatedError, UnauthorizedError


def register_auth_error_handlers(app: FastAPI):
    """Registers all auth error handlers"""
    app.add_exception_handler(UnauthenticatedError, unauthenticated_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)


async def unauthenticated_error_handler(_: Response, __: UnauthenticatedError):
    """Error handler for UnauthenticatedError"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[UnauthenticatedError]},
    )


async def unauthorized_error_handler(_: Response, __: UnauthorizedError):
    """Error handler for UnauthorizedError"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": error_codes[UnauthorizedError]},
    )
