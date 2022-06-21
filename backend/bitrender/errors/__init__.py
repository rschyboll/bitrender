from enum import Enum


class ErrorCode(str, Enum):
    """Error codes returned by errors"""


class AppError(Exception):
    pass
