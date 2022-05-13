"""Contains tests for the TokenHelper class from bitrender.auth.jwt"""

from calendar import timegm
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from pytest_mock import MockerFixture

from bitrender.auth.jwt import TokenHelper


def test_create_decode(mocker: MockerFixture):
    """Tests the that the hash method returns a different hash each time."""
    user_id = uuid4()
    token_helper = TokenHelper()
    now = datetime.utcnow()
    datetime_mock = MagicMock(wraps=datetime)
    datetime_mock.utcnow.return_value = now
    mocker.patch("bitrender.auth.jwt.datetime", datetime_mock)
    token = token_helper.create_token(user_id)
    token_data = token_helper.decode_token(token)
    assert token_data.exp == timegm(now.utctimetuple())
    assert token_data.sub == user_id.hex
