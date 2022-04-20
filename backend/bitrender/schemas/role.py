from bitrender.schemas.base import BaseSchema


class RoleSchema(BaseSchema):
    name: str
    default: bool | None
