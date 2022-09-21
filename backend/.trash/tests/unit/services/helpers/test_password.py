"""Contains tests for the PasswordHelper class from bitrender.auth.password"""
from bitrender.services.helpers.core.password import BCryptHelper


def test_hash_salt() -> None:
    """Tests the that the hash method returns a different hash each time."""
    password_helper = BCryptHelper()
    password = "test_password"
    password_helper.rounds = 4
    assert password_helper.hash(password) != password_helper.hash(password)
