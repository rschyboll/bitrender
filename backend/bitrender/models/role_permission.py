from enum import IntEnum
from typing import TYPE_CHECKING

from tortoise.fields.data import IntEnumField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

if TYPE_CHECKING:
    from bitrender.models.role import Role
else:
    Role = object


class Permission(IntEnum):
    ADD_WORKER = 1
    REMOVE_WORKER = 2
    MANAGE_WORKER = 3
    WORKERS = 4


class RolePermission:
    role: ForeignKeyRelation[Role] = ForeignKeyField("models.Role")
    permission = IntEnumField(Permission)
