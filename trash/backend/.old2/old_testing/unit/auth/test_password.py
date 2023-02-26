"""Contains tests for the PasswordHelper class from bitrender.auth.password"""
import pytest

from bitrender.auth.password import PasswordHelper

password_helper = PasswordHelper()


def test_hash_salt():
    """Tests the that the hash method returns a different hash each time."""
    password = "test"
    password_helper.rounds = 4
    assert password_helper.hash(password) != password_helper.hash(password)


def test_verify():
    """Tests the password verify function."""
    password = "test"
    password_helper.rounds = 4
    hashed_password = password_helper.hash(password)
    assert password_helper.verify(password, hashed_password)
    assert not password_helper.verify("test2", hashed_password)


def test_validate():
    """Tests the password validation function."""
    with pytest.raises(ValueError):
        password_helper.validate("1234567")
    with pytest.raises(ValueError):
        password_helper.validate("abcdefgh")
    with pytest.raises(ValueError):
        password_helper.validate("1234efgh")
    with pytest.raises(ValueError):
        password_helper.validate("1234EFGH")
    password_helper.validate("1234edGH")
