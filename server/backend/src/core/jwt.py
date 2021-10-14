from typing import Dict, Union

from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError

from errors.core.jwt import JWTDecodeException

SECRET_KEY = "1cc0650d3e6c5bfa29647e88778ae4948b7f8d7fa6f7f21f85d58811c11c1843"
ALGORITHM = "HS256"


def create_jwt(data: Dict[str, Union[str, int, bool]]) -> str:
    encoded_jwt: str = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_jwt(encoded_jwt: str) -> Dict[str, str]:
    try:
        data: Dict[str, str] = jwt.decode(
            encoded_jwt,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return data
    except (JWTError, JWTClaimsError) as error:
        raise JWTDecodeException() from error
