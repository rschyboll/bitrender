"""Contains helper classes for hashing and validating passwords."""
from functools import lru_cache

import bcrypt


class BCryptHelper:
    """Helper class for hashing and validating passwords with bcrypt."""

    @staticmethod
    def hash(password: str) -> bytes:
        """Hashes the given passoword with the brypt algorithm.

        Args:
            password (str): Password to hash.

        Returns:
            bytes: Hashed passowrd."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))

    @staticmethod
    def verify(password: str, hashed_password: bytes) -> bool:
        """Checks if the given password corresponds to the given hash.

        Args:
            password (str): Password to check.
            hashed_password (bytes): Hashed password to check against.

        Returns:
            bool: If the password corresponds to the hash."""
        return bcrypt.checkpw(password.encode(), hashed_password)
