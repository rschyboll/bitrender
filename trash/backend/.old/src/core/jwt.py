from typing import TypedDict
from uuid import UUID

from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError

from errors.core.jwt import JWTDecodeException

SECRET_KEY = "1cc0650d3e6c5bfa29647e88778ae4948b7f8d7fa6f7f21f85d58811c11c1843"
ALGORITHM = "HS256"


class JWTData(TypedDict):
    id: UUID
    name: str


def create_jwt(data: JWTData) -> str:
    data_dict = {"id": data["id"].hex, "name": data["name"]}
    encoded_jwt: str = jwt.encode(data_dict, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(encoded_jwt: str) -> JWTData:
    try:
        data_dict = jwt.decode(
            encoded_jwt,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return JWTData(id=UUID(hex=data_dict["id"]), name=data_dict["name"])
    except (JWTError, JWTClaimsError, KeyError) as error:
        raise JWTDecodeException() from error
