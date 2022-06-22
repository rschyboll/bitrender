"""Contains tests for the TokenHelper class from bitrender.auth.jwt"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from bitrender.auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, TokenHelper
from bitrender.errors.user import TokenCorruptedError, TokenExpiredError

token_helper = TokenHelper()


def test_expire(mocker: MockerFixture):
    """Tests that decoding an expired token raises a TokenExpiredError."""
    now = datetime.utcnow() - timedelta(days=1)
    __mock_datetime_utcnow(now, mocker)
    with pytest.raises(TokenExpiredError):
        token = token_helper.create_token(uuid4())
        token_helper.decode_token(token)


def test_corrupted():
    """Tests that decoding an corrupted token raises a TokenCorruptedError."""
    with pytest.raises(TokenCorruptedError):
        token_helper.decode_token("token")


def test_decode(mocker: MockerFixture):
    """Tests correctly encoding and decoding the token."""
    user_id = uuid4()
    now = datetime.utcnow()
    exp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    __mock_datetime_utcnow(now, mocker)
    token = token_helper.create_token(user_id)
    token_data = token_helper.decode_token(token)
    assert token_data.sub == user_id
    assert token_data.exp == int(exp.timestamp())


def __mock_datetime_utcnow(time: datetime, mocker: MockerFixture):
    mock = MagicMock(wraps=datetime)
    mock.utcnow.return_value = time
    mocker.patch("bitrender.auth.jwt.datetime", mock)
