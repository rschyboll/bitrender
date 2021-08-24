from typing import Dict, Tuple
from uuid import UUID

from jose import jwt  # type: ignore

SECRET_KEY = "1cc0650d3e6c5bfa29647e88778ae4948b7f8d7fa6f7f21f85d58811c11c1843"
ALGORITHM = "HS256"


def create_jwt(worker_name: str, worker_id: UUID) -> str:
    jwt_data = {
        "name": worker_name,
        "id": worker_id.hex,
    }
    encoded_jwt: str = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(encoded_jwt: str) -> Tuple[str, UUID]:
    print(encoded_jwt)
    data: Dict[str, str] = jwt.decode(
        encoded_jwt,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
    name = data["name"]
    worker_id = UUID(data["id"])
    return name, worker_id
