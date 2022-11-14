"""Contains error handlers for authentication and authorization errors"""
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

from bitrender.api.handlers import error_codes
from bitrender.errors.role import RoleNameTaken


def register_role_error_handlers(app: FastAPI) -> None:
    """Registers all role error handlers"""
    app.add_exception_handler(RoleNameTaken, role_name_taken_error_handler)


async def role_name_taken_error_handler(_: Response, __: RoleNameTaken) -> JSONResponse:
    """Error handler for RoleNameTaken"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": error_codes[RoleNameTaken]},
    )
