from config import Settings
from core.register import deregister_worker, register_worker
from core.settings import load_settings, remove_settings, save_settings, settings_exist
from errors import ClientException
from errors.register import AlreadyRegisteredError, NotRegisteredError
from core import binaries as BinariesCore


async def register(name: str, server_ip: str) -> None:
    try:
        if settings_exist():
            raise AlreadyRegisteredError()
        token = await register_worker(name, server_ip)
        settings = Settings(token, name, server_ip)
        await save_settings(settings)
    except ClientException as error:
        print(error)


async def deregister() -> None:
    try:
        if not settings_exist():
            raise NotRegisteredError()
        settings = await load_settings()
        await deregister_worker(settings.token, settings.server_ip)
        remove_settings()
    except ClientException as error:
        print(error)


async def run() -> None:
    if not settings_exist():
        raise NotRegisteredError()
    settings = await load_settings()
    app = App(settings)
    await app.run()


class App:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def run(self) -> None:
        if not await BinariesCore.up_to_date():
            pass
