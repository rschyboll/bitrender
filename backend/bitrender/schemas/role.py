from typing import Literal
from uuid import UUID

from pydantic import BaseModel as PydanticBase

from bitrender.models import Permission
from bitrender.schemas.base import BaseSchema


class RoleSchema(BaseSchema):
    name: str
    default: bool | None
    permissions: list[Permission]


class RoleCreate(PydanticBase):
    name: str
    default: bool | None


class RoleUpdate(PydanticBase):
    id: UUID
    name: str | None
    default: Literal[True] | None
    permissions: list[Permission]
