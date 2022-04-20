from bitrender.models import Permission
from bitrender.schemas.base import BaseSchema


class RolePermissionSchema(BaseSchema):
    permission: Permission
