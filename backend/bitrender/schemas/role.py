from uuid import UUID

from pydantic import BaseModel as Schema

from bitrender.models.permission import Permission
from bitrender.schemas.base import BaseSchema


class RoleSchema(BaseSchema):
    name: str
    default: bool


class RoleSchemaFlat(RoleSchema):
    pass


class RoleSchemaPartial(RoleSchema):
    permission_ids: list[UUID]


class RoleSchemaFull(RoleSchema):
    pass


class RoleCreateData(Schema):
    name: str
    permissions: set[Permission]
