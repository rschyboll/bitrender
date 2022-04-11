from __future__ import annotations

from uuid import UUID

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
