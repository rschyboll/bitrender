from typing import TYPE_CHECKING

from bitrender.schemas import BaseView

if TYPE_CHECKING:
    from bitrender.models import Permission, Role
else:
    Permission = object
    Role = object


class RoleHasPermissionView(BaseView):
    permission: Permission
    role: Role | None
