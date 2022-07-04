"""TODO generate docstring"""
from tortoise import Tortoise
from tortoise.transactions import in_transaction

from bitrender.config import tortoise_config
from bitrender.models import Permission, Role, RolePermission, User


async def create_admin_account(password: str, email: str) -> None:
    """Creates a admin account."""
    await Tortoise.init(config=tortoise_config)
    async with in_transaction():
        role = await create_admin_role()
        hashed_password = b""
        if await User.exists(email=email):
            user = await User.get_by_email(email)
            await user.delete()
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=True,
            is_verified=True,
            is_superuser=True,
        )
        await user.save(force_create=True, force_update=True)


async def create_admin_role() -> Role:
    """Creates an admin role with all permissions.

    Returns:
        Role: Created admin role"""
    role = Role(name="admin")
    await role.save()
    await assign_all_permissions(role)
    return role


async def assign_all_permissions(role: Role) -> None:
    """Assigns all available permissions to the provided role.

    Args:
        role (Role): Role to assign the permissions to."""
    for permission in Permission:
        await RolePermission.create(permission=permission, role=role)
