from pydantic import BaseModel as PydanticBase

from bitrender.schemas.base import BaseSchema


class RoleSchema(BaseSchema):
    name: str
    default: bool | None


class RoleCreate(PydanticBase):
    name: str
    default: bool | None
