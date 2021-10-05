import json

from aiohttp import ClientError, ClientSession

from errors.connection import ConnectionException
from errors.register import DeRegistrationFailedError, RegistrationFailedError


async def register_worker(session: ClientSession, url: str, name: str) -> str:
    try:
        async with session.post(url, data=name) as response:
            if response.status != 200:
                raise RegistrationFailedError()
            data = json.loads(await response.text())
            if isinstance(data, str):
                return data
            raise RegistrationFailedError()
    except ClientError as error:
        raise ConnectionException() from error


async def deregister_worker(session: ClientSession, url: str, token: str) -> None:
    headers = {"token": token}
    try:
        async with session.delete(url, headers=headers) as response:
            if response.status != 200:
                raise DeRegistrationFailedError()
    except ClientError as error:
        raise ConnectionException() from error
