import json

import aiohttp

from errors.connection import ConnectionException
from errors.register import DeRegistrationFailedError, RegistrationFailedError


async def register_worker(name: str, server_ip: str) -> str:
    url = server_ip + "/workers/register"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=name) as response:
                if response.status != 200:
                    raise RegistrationFailedError
                data = json.loads(await response.text())
                if isinstance(data, str):
                    return data
                raise RegistrationFailedError
    except (aiohttp.ClientError) as error:
        raise ConnectionException from error


async def deregister_worker(token: str, server_ip: str) -> None:
    url = server_ip + "/workers/deregister"
    headers = {"token": token}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(url) as response:
                if response.status != 200:
                    raise DeRegistrationFailedError
    except (aiohttp.ClientError) as error:
        raise ConnectionException from error
