"""TODO generate docstring"""
from tortoise import Tortoise
from tortoise.transactions import in_transaction

from bitrender.base.auth import hash_password
from bitrender.config import tortoise_config
from bitrender.models import Permission, Role, RolePermission, User


async def create_admin_account(username: str, password: str, email: str):
    """Creates a admin account."""
    await Tortoise.init(config=tortoise_config)
    async with in_transaction():
        role = await create_admin_role()
        hashed_password = hash_password(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
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
    for permission_str in Permission:
        role_permission = RolePermission(name=permission_str, role=role)
        await role_permission.save()
