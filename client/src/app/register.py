from aiohttp import ClientError
import json

from config import DIR, URL, Settings
from errors.connection import ConnectionException
from errors.register import AlreadyRegisteredError, RegistrationFailedError

from app import App


class Register(App):
    def __init__(self, name: str, server_ip: str, data_dir: str):
        super(Register, self).__init__()
        self.name = name
        self.server_ip = server_ip
        self.data_dir = data_dir
        self.directories = DIR(data_dir)
        self.urls = URL(server_ip)
        self.settings = Settings(self.directories.settings_file)

    async def _run(self) -> None:
        if self.settings.exist():
            raise AlreadyRegisteredError()
        token = await self.__register()
        self.__save_settings(self.name, self.server_ip, token)

    async def __register(self) -> str:
        url = self.urls.register
        name = self.name
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

    async def _rollback(self) -> None:
        self.__remove_settings()

    def __save_settings(self, name: str, server_ip: str, token: str) -> None:
        self.settings.name = name
        self.settings.server_ip = server_ip
        self.settings.token = token
        self.settings.save()

    def __remove_settings(self) -> None:
        self.settings.delete()
