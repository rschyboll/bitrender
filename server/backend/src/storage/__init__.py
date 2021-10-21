from aerich import Command
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import get_tortoise_config


def register_db(app: FastAPI) -> None:
    config = get_tortoise_config()
    register_tortoise(app, config=config, add_exception_handlers=True)


async def migrate() -> None:
    config = get_tortoise_config()
    command = Command(
        tortoise_config=config,
        app="rendering_server",
        location="../migrations",
    )
    await command.init()
    try:
        await command.init_db(True)
    except FileExistsError:
        pass
    await command.upgrade()
