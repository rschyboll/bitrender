from aerich import Command
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import get_tortoise_config

from .binary import Binary
from .composite_assign import CompositeAssign
from .composite_task import CompositeTask
from .frame import Frame
from .subtask import Subtask
from .subtask_assign import SubtaskAssign
from .task import Task
from .test import Test
from .worker import Worker


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
    try:
        await command.migrate()
    except Exception as error:
        print(error)
    try:
        await command.upgrade()
    except Exception as error:
        print(error)
