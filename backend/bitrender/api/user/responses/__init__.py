from typing import Any

from fastapi import status
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from bitrender.errors.user import UnauthenticatedError, UnauthorizedError, UserNotVerified

error_codes = {
    DoesNotExist: "RESOURCE_NOT_FOUND",
    UnauthenticatedError: "NOT_AUTHENTICATED",
    UnauthorizedError: "NOT_AUTHORIZED",
    UserNotVerified: "USER_NOT_VERIFIED",
}


class ErrorResponseModel(BaseModel):
    detail: str | dict[str, str]


user_me_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthenticatedError]: {
                        "summary": "User could not be authenticated",
                        "value": {"detail": error_codes[UnauthenticatedError]},
                    },
                    error_codes[UnauthorizedError]: {
                        "summary": "User has no access to the requested resource",
                        "value": {"detail": error_codes[UnauthorizedError]},
                    },
                }
            }
        },
    }
}

user_by_id_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[DoesNotExist]: {
                        "summary": "The requested user does not exist.",
                        "value": {"detail": error_codes[DoesNotExist]},
                    }
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthenticatedError]: {
                        "summary": "User could not be authenticated",
                        "value": {"detail": error_codes[UnauthenticatedError]},
                    },
                    error_codes[UnauthorizedError]: {
                        "summary": "User has no access to the requested resource",
                        "value": {"detail": error_codes[UnauthorizedError]},
                    },
                }
            }
        },
    },
}

user_login_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UserNotVerified]: {
                        "summary": "The user is not verified",
                        "value": {"detail": error_codes[UserNotVerified]},
                    },
                }
            }
        },
    }
}
