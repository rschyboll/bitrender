# pylint: disable=missing-module-docstring

from .base import BaseModel  # noqa: F401
from .permission import Permission, RoleHasPermission  # noqa: F401
from .role import Role  # noqa: F401


async def init_db_data():
    """Populates database with initial data."""


async def create_admin_role():
    role = Role(
        name="admin",
    )
