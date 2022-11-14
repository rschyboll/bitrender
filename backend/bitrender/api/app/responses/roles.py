"""Contains responses for the routes in the roles_router"""
from typing import Any

from fastapi import status
from tortoise.exceptions import DoesNotExist

from bitrender.api.handlers import error_codes
from bitrender.errors.user import UnauthorizedError

from . import ErrorResponseModel

roles_get_list: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthorizedError]: {
                        "summary": "User has no access to the requested resource",
                        "value": {"detail": error_codes[UnauthorizedError]},
                    },
                }
            }
        },
    },
}

roles_get_by_id: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthorizedError]: {
                        "summary": "User has no access to the requested resource",
                        "value": {"detail": error_codes[UnauthorizedError]},
                    },
                    error_codes[DoesNotExist]: {
                        "summary": "The requested role does not exist.",
                        "value": {"detail": error_codes[DoesNotExist]},
                    },
                }
            }
        },
    },
}
