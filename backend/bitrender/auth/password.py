"""Contains helper classes for hashing and validating passwords."""

import bcrypt


class PasswordHelper:
    """Class with helper methods for password management."""

    rounds = 14

    def hash(self, password: str) -> bytes:
        """Hashes the given passoword with the brypt algorithm.

        Args:
            password (str): Password to hash.

        Returns:
            bytes: Hashed passowrd."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(self.rounds))

    @staticmethod
    def verify(password: str, hashed_password: bytes) -> bool:
        """Checks if the given password corresponds to the given hash.

        Args:
            password (str): Password to check.
            hashed_password (bytes): Hashed password to check against.

        Returns:
            bool: If the password corresponds to the hash."""
        return bcrypt.checkpw(password.encode(), hashed_password)

    @staticmethod
    def validate(password: str):
        """Validates if the password is secure enough.

        Args:
            password (str): Password to validate.

        Raises:
            ValueError: Raised when the password does not meet the requirements"""
        if len(password) < 8:
            raise ValueError("Password length should be at least 8")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            raise ValueError("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password should have at least one lowercase letter")
