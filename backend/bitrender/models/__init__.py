"""Reexports all models from it's submodules and contains utilitymethods for TortoiseORM"""

import aerich

from bitrender.config import tortoise_config

from .base import BaseModel
from .permission import RolePermission
from .role import Role
from .user import User

__all__ = ["BaseModel", "RolePermission", "Role", "User"]


async def __create_aerich_command() -> aerich.Command:
    command = aerich.Command(
        tortoise_config=tortoise_config,
        app="bitrender",
    )
    await command.init()
    return command


async def init_db() -> None:
    """Initializes the database, creates all tables and relations based on models."""
    command = await __create_aerich_command()
    await command.init_db(True)


async def migrate() -> None:
    """Migrates the database based on current models."""
    command = await __create_aerich_command()
    await command.migrate()
    await command.upgrade()
