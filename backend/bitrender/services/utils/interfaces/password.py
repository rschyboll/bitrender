"""Contains interface for the password helper implementations."""
from abc import ABC

from antidote import interface
from pyparsing import abstractmethod


@interface
class IPasswordHelper(ABC):
    """Interface for classes for hashing, verifying and validating passwords."""

    @abstractmethod
    def hash(self, password: str) -> bytes:
        """Hashes the given password.

        Args:
            password (str): Password to hash.

        Returns:
            bytes: Hashed password."""

    @abstractmethod
    def verify(self, password: str, hashed_password: bytes) -> bool:
        """Checks if the given password corresponds to the given hash.

        Args:
            password (str): Password to check.
            hashed_password (bytes): Hashed password to check against.

        Returns:
            bool: If the password corresponds to the hash."""

    @abstractmethod
    def validate(self, password: str):
        """Validates if the password is secure enough.

        Args:
            password (str): Password to validate.

        Raises:
            ValueError: Raised when the password does not meet the requirements"""
