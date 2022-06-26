"""Contains interface for the token helper implementations."""
from abc import ABC
from datetime import timedelta
from uuid import UUID

from antidote import interface

from bitrender.schemas.user import UserTokenData


@interface
class ITokenHelper(ABC):
    """Interface for classes for creating and managing web tokens."""

    def create(self, data: dict, expires_delta: timedelta) -> str:
        """Creates a JWT token containing the given data.

        Args:
            data (dict): Dict to include in the token.

        Raises:
            TokenCreateError: If there is an error creating the token.

        Returns:
            str: Created JWT"""

    def decode(self, token: str) -> dict:
        """Decodes the token and returns the data that was in it.

        Args:
            token (str): JWT that should be decoded.

        Raises:
            TokenExpiredError: Raised when the token has expired.
            TokenCorruptedError: Raised when could not decode the token.

        Returns:
            dict: Data that was contained within the JWT"""

    def create_user_token(self, sub: UUID) -> str:
        """Creates a JWT token containing user id data.

        Args:
            user_id (UUID): Id of the user

        Raises:
            TokenCreateError: If there is an error creating the token.

        Returns:
            str: Created JWT"""

    def decode_user_token(self, token: str) -> UserTokenData:
        """Decodes the user JWT token and returns the signed user data.

        Args:
            token (str): JWT that should be decoded.

        Raises:
            TokenExpiredError: Raised when the token has expired.
            TokenCorruptedError: Raised when could not decode the token.

        Returns:
            TokenData: Data that was contained within the JWT"""
