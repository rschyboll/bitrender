from typing import Any

from fastapi import status
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    detail: str | dict[str, str]


user_get_me_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_401_UNAUTHORIZED: {"model": {}}
}
