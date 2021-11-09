import json
from typing import Any

from aiohttp import ClientError

from app.action import Action
from config import URL, Settings
from errors.connection import ConnectionException
from errors.register import RegistrationFailedError


class RegisterWorker(Action[None]):
    background = False
    critical = True

    def __init__(self, settings: Settings, urls: URL, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls

    async def _start(self) -> None:
        assert self.settings.server_ip is not None
        assert self.settings.name is not None
        token = await self.__register(self.urls.register, self.settings.name)
        self.settings.token = token
        self.settings.save()

    async def __register(self, url: str, name: str) -> str:
        try:
            async with self.session.post(url, data=name) as response:
                if response.status != 200:
                    raise RegistrationFailedError()
                data = json.loads(await response.text())
                if isinstance(data, str):
                    return data
                raise RegistrationFailedError()
        except ClientError as error:
            raise ConnectionException() from error

    async def _local_rollback(self) -> None:
        self.settings.delete()

    async def _rollback(self) -> None:
        pass


class DeregisterWorker(Action[None]):
    background = False
    critical = True

    def __init__(self, settings: Settings, urls: URL, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls

    async def _start(self) -> None:
        assert self.settings.server_ip is not None
        assert self.settings.name is not None
        await self.__deregister()
        self.settings.delete()

    async def __deregister(self) -> None:
        try:
            async with self.session.delete(
                self.urls.deregister, headers={"token": self.settings.token}
            ) as response:
                if response.status != 200:
                    pass
        except ClientError as error:
            raise ConnectionException() from error

    async def _local_rollback(self) -> None:
        self.settings.delete()

    async def _rollback(self) -> None:
        pass
