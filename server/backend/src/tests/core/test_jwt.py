from typing import Dict, Union

import pytest

from core import jwt
from errors.core.jwt import JWTDecodeException


def test_create_decode_jwt() -> None:
    data: Dict[str, Union[str, int, bool]] = {"key1": 32, "key2": "test", "key3": True}
    token = jwt.create_jwt(data)
    decoded_data = jwt.decode_jwt(token)
    assert data == decoded_data


def test_decode_jwt_throws() -> None:
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn9Klv_0x0vk32T1z4PFqZaKDeF2DFacQJiOxqjXG3S48"
    with pytest.raises(JWTDecodeException):
        jwt.decode_jwt(token)
