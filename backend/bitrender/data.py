from tortoise import Tortoise

from bitrender.base.auth import hash_password
from bitrender.config import tortoise_config
from bitrender.models import User
from bitrender.models.permission import Permission, RoleHasPermission
from bitrender.models.role import Role


async def create_admin_account(username: str, password: str, email: str):
    """Creates a admin account."""
    await Tortoise.init(config=tortoise_config)
    role = await create_admin_role()
    password_hash = hash_password(password)
    user = User(
        username=username,
        password_hash=password_hash,
        email=email,
        role=role,
    )
    await user.save()


async def create_admin_role() -> Role:
    """Creates an admin role with all permissions.

    Returns:
        Role: Created admin role"""
    role = Role(name="admin")
    await role.save()
    await assign_all_permissions(role)
    return role


async def assign_all_permissions(role: Role):
    """Assigns all available permissions to the provided role.

    Args:
        role (Role): Role to assign the permissions to."""
    for permission in Permission:
        role_permission = RoleHasPermission(permission, role)
        await role_permission.save()
