"""Contains implementation for the IPasswordHelper interface."""

import bcrypt
from antidote import implements

from bitrender.services.helpers.interfaces.password import IPasswordHelper


@implements(IPasswordHelper)
class BCryptHelper(IPasswordHelper):
    """Helper class containing implementation for hashing, verifying and validating passwords."""

    rounds = 14
    special_characters = """!@#$%^&*()-+?_=,<>/"""

    def hash(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(self.rounds))

    def verify(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)

    def validate(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password length should be at least 8")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password should have at least one numeral")

        if not any(char in self.special_characters for char in password):
            raise ValueError("Password should have at least one special character")

        if not any(char.isupper() for char in password):
            raise ValueError("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password should have at least one lowercase letter")
