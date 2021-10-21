from aiohttp import ClientSession
from websockets.client import connect
import json
from typing import Dict
from multiprocessing import shared_memory

from app import App
from config import DIR, URL, Settings
from errors.config import SettingsReadError
from errors.register import NotRegisteredError
from core.binary import Binary
from core.actions import Action, ActionType


class Worker(App):
    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir
        self.directories = DIR(data_dir)
        self.settings = Settings(self.directories.settings_file)
        self.urls = URL()
        self.binary = Binary(self.directories, self.settings, self.urls)
        self.tasks = shared_memory.SharedMemory()

    async def _run(self, session: ClientSession) -> None:
        self.__read_settings()
        await self.__get_binaries(session)
        await self.__connect_to_server(session)

    def __read_settings(self) -> None:
        if not self.settings.exist():
            raise NotRegisteredError()
        try:
            self.settings.read()
            self.urls.set_server_ip(self.settings.server_ip)
        except SettingsReadError as error:
            raise NotRegisteredError() from error

    async def __start_file_system(self) -> None:
        pass

    async def __get_binaries(self, session: ClientSession) -> None:
        try:
            if not (await self.binary.up_to_date(session) and self.binary.exists()):
                await self.binary.download_new_version(session)
        except:
            self.binary.delete()
            raise

    async def __connect_to_server(self, session: ClientSession):
        headers = {"token": self.settings.token}
        async with connect(self.urls.websocket, extra_headers=headers) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    action = Action.from_json(message)
                    if action.type == ActionType.TEST:
                        await self.download_test_task(session)
                except Exception as error:
                    pass

    async def download_test_task(self, session: ClientSession):
        async with session.get(self.urls.test_task) as response:
            self.tasks["test"] = await response.content.read()

    def choose_action(self, message: str):
        pass

    async def _rollback(self) -> None:
        pass
