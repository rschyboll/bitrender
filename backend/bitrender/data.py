"""TODO generate docstring"""
from antidote import inject
from tortoise import Tortoise
from tortoise.transactions import in_transaction

from bitrender.app import init_deps
from bitrender.config import tortoise_config
from bitrender.models import Permission, Role, RolePermission, User
from bitrender.services.helpers.interfaces.password import IPasswordHelper

init_deps()


@inject
async def create_admin_account(
    password: str, email: str, password_helper: IPasswordHelper = inject.me()
) -> None:
    """Creates an admin account."""
    await Tortoise.init(config=tortoise_config)
    async with in_transaction():
        role = await create_admin_role()
        hashed_password = password_helper.hash(password)
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
