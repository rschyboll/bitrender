import os
import aiohttp
from errors.connection import ConnectionException

from appdirs import user_data_dir  # type: ignore
from config import Config

data_dir = user_data_dir(Config.app_name, Config.app_author)
binary_dir = os.path.join(data_dir, Config.binary_directory)


async def up_to_date() -> bool:
    if not os.path.exists(binary_dir):
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                if response.status != 200:
                    raise DeRegistrationFailedError
    except (aiohttp.ClientError) as error:
        raise ConnectionException from error
