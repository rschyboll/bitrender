from aiohttp import ClientSession

from config import DIR, URL, Settings
from core.register import deregister_worker
from errors.register import NotRegisteredError


class Deregister:
    def __init__(self, directories: DIR, settings: Settings, urls: URL):
        self.directories = directories
        self.settings = settings
        self.urls = urls

    async def deregister(self) -> None:
        try:
            if not self.settings.exist():
                raise NotRegisteredError()
            async with ClientSession() as session:
                await deregister_worker(
                    session, self.urls.deregister, self.settings.token
                )
                self.__remove_settings()
        except Exception:
            await self.__rollback_deregister()
            raise

    def __remove_settings(self) -> None:
        self.settings.delete()

    async def __rollback_deregister(self) -> None:
        pass
