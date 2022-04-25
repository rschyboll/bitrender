from enum import Enum

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: str | dict[str, str]


class ErrorCode(str, Enum):
    NO_DEFAULT_ROLE = "NO_DEFAULT_ROLE"
    REGISTER_USER_ALREADY_EXISTS = "REGISTER_USER_ALREADY_EXISTS:"
    LOGIN_BAD_CREDENTIALS = "LOGIN_BAD_CREDENTIALS"
    LOGIN_USER_NOT_VERIFIED = "LOGIN_USER_NOT_VERIFIED"
