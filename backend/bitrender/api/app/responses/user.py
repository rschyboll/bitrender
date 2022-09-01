from typing import Any

from fastapi import status
from tortoise.exceptions import DoesNotExist

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

from . import ErrorResponseModel

user_login_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UserNotVerified]: {
                        "summary": "The user is not verified",
                        "value": {"detail": error_codes[UserNotVerified]},
                    },
                    error_codes[BadCredentials]: {
                        "summary": "Could not authenticate a user with those credentials",
                        "value": {"detail": error_codes[BadCredentials]},
                    },
                }
            }
        },
    },
}

user_register_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_409_CONFLICT: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UsernameTaken]: {
                        "summary": "User with that username already exists",
                        "value": {"detail": error_codes[UsernameTaken]},
                    },
                    error_codes[EmailTaken]: {
                        "summary": "User with that email already exists",
                        "value": {"detail": error_codes[EmailTaken]},
                    },
                }
            }
        },
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[NoDefaultRole]: {
                        "summary": "No default role is selected in the system",
                        "value": {"detail": error_codes[NoDefaultRole]},
                    },
                }
            }
        },
    },
}

user_me_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthenticatedError]: {
                        "summary": "User is not authenticated",
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

user_logged_responses: dict[int | str, dict[str, Any]] = {}

user_logout_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponseModel,
        "content": {
            "application/json": {
                "examples": {
                    error_codes[UnauthenticatedError]: {
                        "summary": "User is not authenticated",
                        "value": {"detail": error_codes[UnauthenticatedError]},
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
