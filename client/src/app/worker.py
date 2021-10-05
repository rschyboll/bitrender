from aiohttp import ClientSession

from config import DIR, URL, Settings
from core import binaries as BinariesCore


class App:
    def __init__(self, directories: DIR, settings: Settings, urls: URL):
        self.directories = directories
        self.settings = settings
        self.urls = urls
        self.session = ClientSession()

    async def run(self) -> None:
        try:
            if not self.settings.exist() and not self.settings.validate_settings():
                return
            if not await BinariesCore.up_to_date(self.settings.server_ip):
                await BinariesCore.update_binary(self.settings.server_ip)
        finally:
            self.session.close()

    async def check_settings(self):
        pass

    async def check_binary(self):
        pass
