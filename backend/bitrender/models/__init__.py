# pylint: disable=missing-module-docstring

import aerich

from bitrender.config import tortoise_config

from .auth import UserAuth  # noqa: F401
from .permission import Permissions, RoleHasPermission  # noqa: F401
from .role import Role  # noqa: F401
from .user import User  # noqa: F401


async def __create_aerich_command() -> aerich.Command:
    command = aerich.Command(
        tortoise_config=tortoise_config,
        app="bitrender",
    )
    await command.init()
    return command


async def init_db():
    """Initializes the database, creates all tables and relations based on models."""
    command = await __create_aerich_command()
    await command.init_db()


async def migrate():
    """Migrates the database based on current models."""
    command = await __create_aerich_command()
    await command.migrate()
    await command.upgrade()
