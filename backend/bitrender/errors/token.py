"""Contains all errors related to creating and decoding web tokens."""
from bitrender.errors import AppError


class TokenError(AppError):
    """Base error for all errors related to creating and decoding web tokens."""


class TokenCreateError(TokenError):
    """Raised, when the creation of a web token failed."""


class TokenCorruptedError(TokenError):
    """Raised when the received auth token got corrupted"""


class TokenExpiredError(TokenError):
    """Raised when the received auth token is expired"""
