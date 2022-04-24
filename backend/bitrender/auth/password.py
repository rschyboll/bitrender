"""Contains helper classes for hashing and validating passwords."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the given passoword with the brypt algorithm.

    Args:
        password (str): Password to hash.

    Returns:
        bytes: Hashed passowrd."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Checks if the given password corresponds to the given hash.

    Args:
        password (str): Password to check.
        hashed_password (bytes): Hashed password to check against.

    Returns:
        bool: If the password corresponds to the hash."""
    return bcrypt.checkpw(password.encode(), hashed_password)


def validate_password(password: str):
    """Validates that the password is secure enough."""
    if len(password) < 8:
        raise ValueError("Password length should be at least 8")

    if not any(char.isdigit() for char in password):
        raise ValueError("Password should have at least one numeral")

    if not any(char.isupper() for char in password):
        raise ValueError("Password should have at least one uppercase letter")

    if not any(char.islower() for char in password):
        raise ValueError("Password should have at least one lowercase letter")
