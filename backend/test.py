import asyncio

from tortoise import Tortoise

from bitrender.config import tortoise_config
from tests.utils.generators import generate_roles


async def test() -> None:
    await Tortoise.init(tortoise_config)
    await generate_roles(250)


asyncio.run(test())
