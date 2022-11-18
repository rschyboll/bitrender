from typing import Literal
from uuid import UUID

from pydantic import BaseModel as PydanticBase
from pydantic import validator

from bitrender.enums.permission import Permission
from bitrender.schemas.base import BaseSchema


class RoleView(BaseSchema):
    name: str
    default: Literal[True] | None
    permissions: list[Permission]


class RoleCreate(PydanticBase):
    name: str
    default: Literal[True] | None
    permissions: list[Permission]

    @validator("name")
    @classmethod
    def name_validator(cls, name: str) -> None:
        """Validates that the name is at least 4 letters length."""
        if len(name) < 4:
            raise ValueError("Role name has to contain at least 4 letters.")


class RoleUpdate(PydanticBase):
    id: UUID
    name: str | None
    default: Literal[True] | None
    permissions: list[Permission] | None
