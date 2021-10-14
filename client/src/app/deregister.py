from aiohttp import ClientError, ClientSession

from app import App
from config import DIR, URL, Settings
from errors.config import SettingsReadError
from errors.connection import ConnectionException
from errors.register import NotRegisteredError


class Deregister(App):
    def __init__(self, data_dir: str):
        super(Deregister, self).__init__()
        self.data_dir = data_dir
        self.directories = DIR(data_dir)
        self.settings = Settings(self.directories.settings_file)
        self.urls = URL()

    async def _run(self, session: ClientSession) -> None:
        if not self.settings.exist():
            raise NotRegisteredError()
        try:
            self.settings.read()
            self.urls.set_server_ip(self.settings.server_ip)
        except SettingsReadError as error:
            raise NotRegisteredError() from error
        await self.__deregister(session)
        self.settings.delete()

    async def __deregister(self, session: ClientSession) -> None:
        headers = {"token": self.settings.token}
        try:
            async with session.delete(
                self.urls.deregister, headers=headers
            ) as response:
                if response.status != 200:
                    pass
        except ClientError as error:
            raise ConnectionException() from error

    async def _rollback(self) -> None:
        pass
