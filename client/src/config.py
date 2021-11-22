import os
from configparser import ConfigParser, NoOptionError, NoSectionError, ParsingError
from typing import Optional
from uuid import UUID

from errors.config import SettingsNotReadError, SettingsReadError, SettingsWriteError


class Config:
    app_name = "rendering_server_worker"
    app_author = "hoodrobinrs"


class Settings:
    settings_section = "settings"
    blender_section = "blender"

    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.__config_parser = ConfigParser()

    def read(self) -> None:
        try:
            read_files = self.__config_parser.read(self.settings_file)
            if len(read_files) == 0 or not self.validate_settings():
                raise SettingsReadError()
        except ParsingError as error:
            raise SettingsReadError() from error

    def save(self) -> None:
        if not self.validate_settings():
            raise SettingsWriteError()
        try:
            settings_directory = os.path.dirname(self.settings_file)
            if not os.path.exists(settings_directory):
                os.makedirs(settings_directory, exist_ok=True)
            with open(self.settings_file, "w+", encoding="utf-8") as configfile:
                self.__config_parser.write(configfile)
        except OSError as error:
            raise SettingsWriteError() from error

    def delete(self) -> None:
        try:
            if os.path.exists(self.settings_file):
                self.__config_parser.clear()
                os.remove(self.settings_file)
        except OSError:
            pass

    def exist(self) -> bool:
        return os.path.exists(self.settings_file)

    def validate_settings(self) -> bool:
        try:
            return (
                self.token is not None
                and self.name is not None
                and self.server_ip is not None
            )
        except SettingsNotReadError:
            return False

    @property
    def token(self) -> str:
        return self.__get_key(self.settings_section, "token")

    @token.setter
    def token(self, value: str) -> None:
        self.__set_key(self.settings_section, "token", value)

    @property
    def name(self) -> str:
        return self.__get_key(self.settings_section, "name")

    @name.setter
    def name(self, value: str) -> None:
        self.__set_key(self.settings_section, "name", value)

    @property
    def server_ip(self) -> str:
        return self.__get_key(self.settings_section, "server_ip")

    @server_ip.setter
    def server_ip(self, value: str) -> None:
        self.__set_key(self.settings_section, "server_ip", value)

    @property
    def blender_version(self) -> Optional[str]:
        return self.__get_key_optional(self.blender_section, "blender_version")

    @blender_version.setter
    def blender_version(self, value: Optional[str]) -> None:
        self.__set_key_optional(self.blender_section, "blender_version", value)

    def __set_key(self, section: str, option: str, value: str) -> None:
        if not self.__config_parser.has_section(section):
            self.__config_parser.add_section(section)
        self.__config_parser.set(section, option, value)

    def __get_key(self, section: str, option: str) -> str:
        try:
            return self.__config_parser.get(section, option)
        except (NoSectionError, NoOptionError) as error:
            raise SettingsNotReadError from error

    def __get_key_optional(self, section: str, option: str) -> Optional[str]:
        return self.__config_parser.get(section, option, fallback=None)

    def __set_key_optional(
        self, section: str, option: str, value: Optional[str]
    ) -> None:
        if not self.__config_parser.has_section(section):
            self.__config_parser.add_section(section)
        if value is None:
            self.__config_parser.remove_option(section, option)
        else:
            self.__config_parser.set(section, option, value)

    @property
    def properties(self) -> list[str]:
        class_items = self.__class__.__dict__.items()
        return [
            k for k, v in class_items if isinstance(v, property) and k != "properties"
        ]


class URL:
    def __init__(self, server_ip: str = "127.0.0.1:8000"):
        self.server_ip = server_ip

    def set_server_ip(self, server_ip: str) -> None:
        self.server_ip = server_ip

    @property
    def register(self) -> str:
        return f"http://{self.server_ip}/workers/register"

    @property
    def deregister(self) -> str:
        return f"http://{self.server_ip}/workers/deregister"

    @property
    def websocket(self) -> str:
        return f"ws://{self.server_ip}/ws"

    @property
    def binary(self) -> str:
        return f"http://{self.server_ip}/binaries/latest"

    @property
    def test_task(self) -> str:
        return f"http://{self.server_ip}/tasks/test_task"

    def task(self, task_id: UUID) -> str:
        return f"http://{self.server_ip}/tasks/file/{task_id.hex}"

    @property
    def subtask_success(self) -> str:
        return f"http://{self.server_ip}/subtasks/success"

    @property
    def subtask_error(self) -> str:
        return f"http://{self.server_ip}/subtasks/error"


class DIR:
    def __init__(self, data_dir: str = "./"):
        self.data_dir = data_dir

    def set_data_dir(self, data_dir: str) -> None:
        self.data_dir = data_dir

    @property
    def settings_file(self) -> str:
        return os.path.join(self.data_dir, "settings.json")

    @property
    def download_file(self) -> str:
        return os.path.join(self.data_dir, "blender.tar.xz")

    @property
    def binary_dir(self) -> str:
        return os.path.join(self.data_dir, "blender/")

    @property
    def binary(self) -> str:
        return os.path.join(self.binary_dir + "blender")

    def binary_tar(self, tempdir: str) -> str:
        return os.path.join(tempdir, "download.tar.xz")

    @property
    def task_dir(self) -> str:
        return os.path.join(self.data_dir, "tasks/")

    @property
    def render_scripts_dir(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "rendering_api/"
        )

    @property
    def blender_config_dir(self) -> str:
        return os.path.join(self.data_dir, "blender_config/")

    @property
    def render_script(self) -> str:
        return os.path.join(self.render_scripts_dir, "render.py")
