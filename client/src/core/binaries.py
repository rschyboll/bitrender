import aiohttp
from errors.connection import ConnectionException
from core.settings import load_current_version


async def up_to_date(server_ip: str) -> bool:
    url = server_ip + "/binaries/latest"
    version = await load_current_version()
    if version is None:
        return False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                if data != version:
                    return False
                return True
    except (aiohttp.ClientError) as error:
        raise ConnectionException from error


async def update_binary(server_ip: str) -> bool:
    url = server_ip + "/binaries/latest"
