"""Contains tests for the BCryptHelper class from bitrender.services.helpers.core.password"""
import pytest

from bitrender.services.helpers.core.password import BCryptHelper


def test_hash_salt() -> None:
    """Tests the that the hash method returns a different hash each time."""
    password_helper = BCryptHelper()
    password = "test"
    password_helper.rounds = 4
    assert password_helper.hash(password) != password_helper.hash(password)


def test_verify() -> None:
    """Tests the password verify function."""
    password_helper = BCryptHelper()
    password = "test"
    password_helper.rounds = 4
    hashed_password = password_helper.hash(password)
    assert password_helper.verify(password, hashed_password)
    assert not password_helper.verify("test2", hashed_password)


def test_validate() -> None:
    """Tests the password validation function."""
    password_helper = BCryptHelper()
    with pytest.raises(ValueError):
        password_helper.validate("1234567")
    with pytest.raises(ValueError):
        password_helper.validate("abcdefgh#")
    with pytest.raises(ValueError):
        password_helper.validate("1234efgh#")
    with pytest.raises(ValueError):
        password_helper.validate("1234EFGH#")
    with pytest.raises(ValueError):
        password_helper.validate("1234EFGHh")
    password_helper.validate("1234ed#GH")
