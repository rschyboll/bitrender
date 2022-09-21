from typing import Literal
from uuid import UUID

from pydantic import BaseModel as PydanticBase

from bitrender.enums.permission import Permission
from bitrender.schemas.base import BaseSchema


class RoleView(BaseSchema):
    name: str
    default: Literal[True] | None
    permissions: list[Permission]


class RoleCreate(PydanticBase):
    name: str
    default: Literal[True] | None


class RoleUpdate(PydanticBase):
    id: UUID
    name: str | None
    default: Literal[True] | None
    permissions: list[Permission]
