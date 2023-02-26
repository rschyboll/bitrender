from appdirs import user_data_dir

from app.action import Action
from config import DIR, URL, Config, Settings
from errors.register import AlreadyRegisteredError, NotRegisteredError


def _get_urls(server_ip: str) -> URL:
    return URL(server_ip)


def _get_settings(directories: DIR) -> Settings:
    return Settings(directories.settings_file)


def _get_directories() -> DIR:
    data_dir = user_data_dir(Config.app_name, Config.app_author)
    return DIR(data_dir)


class GetWorkerConfig(Action[None]):
    critical = True
    background = False

    async def _start(self) -> None:
        self.state.directories = _get_directories()
        self.state.settings = _get_settings(self.state.directories)
        if not self.state.settings.exist():
            raise NotRegisteredError()
        self.state.settings.read()
        self.state.urls = _get_urls(self.state.settings.server_ip)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class GetRegisterConfig(Action[None]):
    critical = True
    background = False

    async def _start(self) -> None:
        assert "server_ip" in self.kwargs
        assert "name" in self.kwargs
        self.state.directories = _get_directories()
        self.state.settings = _get_settings(self.state.directories)
        if self.state.settings.exist():
            raise AlreadyRegisteredError()
        self.state.urls = _get_urls(self.kwargs["server_ip"])
        self.__save_kwargs(self.state.settings)

    def __save_kwargs(self, settings: Settings) -> None:
        settings.server_ip = self.kwargs["server_ip"]
        settings.name = self.kwargs["name"]

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass
