from typing import TYPE_CHECKING

from bitrender.schemas import BaseView

if TYPE_CHECKING:
    from bitrender.models import Permissions, Role
else:
    Permissions = object
    Role = object


class RoleHasPermissionView(BaseView):
    permission: Permissions
    role: Role | None
