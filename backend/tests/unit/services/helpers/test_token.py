"""Contains tests for the TokenHelper class from bitrender.auth.jwt"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from bitrender.config import get_settings
from bitrender.errors.token import TokenCorruptedError, TokenCreateError, TokenExpiredError
from bitrender.services.helpers.core.token import TokenHelper, UserTokenData


def test_expire(mocker: MockerFixture) -> None:
    """Tests that decoding an expired token raises a TokenExpiredError."""
    token_helper = TokenHelper()
    now = datetime.utcnow() - timedelta(days=1)
    __mock_datetime_utcnow(now, mocker)
    with pytest.raises(TokenExpiredError):
        token = token_helper.create({"sub": uuid4().hex}, timedelta(minutes=30))
        token_helper.decode(token)


def test_corrupted() -> None:
    """Tests that decoding an corrupted token raises a TokenCorruptedError."""
    token_helper = TokenHelper()
    with pytest.raises(TokenCorruptedError):
        token_helper.decode("token")


def test_create_error() -> None:
    """Tests that creating a jwt with wrong data raises a TokenCreateError"""
    token_helper = TokenHelper()
    with pytest.raises(TokenCreateError):
        token_helper.create({"sub": uuid4()}, timedelta(minutes=30))


def test_decode(mocker: MockerFixture) -> None:
    """Tests correctly encoding and decoding the token."""
    token_helper = TokenHelper()
    user_id = uuid4()
    now = datetime.utcnow()
    exp = now + timedelta(minutes=30)
    __mock_datetime_utcnow(now, mocker)
    token = token_helper.create({"sub": user_id.hex}, timedelta(minutes=30))
    token_data = token_helper.decode(token)
    assert token_data["sub"] == user_id.hex
    assert token_data["exp"] == int(exp.timestamp())


def test_create_decode_user_token() -> None:
    """Tests the create and decode user token methods"""
    settings = get_settings()
    token_helper = TokenHelper()
    uuid = uuid4()
    token = token_helper.create_user_token(uuid, settings)
    token_data = token_helper.decode_user_token(token)
    assert isinstance(token_data, UserTokenData)
    assert token_data.sub.hex == uuid.hex


def test_decode_user_token_corrupted() -> None:
    """Tests that the decode_user_token raises TokenCorruptedError on wrong token data"""
    token_helper = TokenHelper()
    with pytest.raises(TokenCorruptedError):
        token = token_helper.create({"test": 1}, timedelta(minutes=30))
        token_helper.decode_user_token(token)


def __mock_datetime_utcnow(time: datetime, mocker: MockerFixture) -> None:
    mock = MagicMock(wraps=datetime)
    mock.utcnow.return_value = time
    mocker.patch("bitrender.services.helpers.core.token.datetime", mock)
