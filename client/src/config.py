import os
from configparser import ConfigParser, NoOptionError, NoSectionError, ParsingError
from typing import Optional

from errors.settings import SettingsNotReadError, SettingsReadError, SettingsWriteError


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
            if len(read_files) == 0:
                raise SettingsReadError()
            if not self.validate_settings():
                raise SettingsReadError()
        except ParsingError as error:
            raise SettingsReadError() from error

    def save(self) -> None:
        if not self.validate_settings():
            raise SettingsWriteError()
        try:
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
        return self.__get_key_optional(self.settings_section, "blender_version")

    @blender_version.setter
    def blender_version(self, value: str) -> None:
        self.__set_key(self.blender_section, "blender_version", value)

    def __set_key(self, section: str, option: str, value: str) -> None:
        if self.__config_parser.has_section(section):
            self.__config_parser.set(section, option, value)
        else:
            self.__config_parser.add_section(section)
            self.__config_parser.set(section, option, value)

    def __get_key(self, section: str, option: str) -> str:
        try:
            return self.__config_parser.get(section, option)
        except (NoSectionError, NoOptionError) as error:
            raise SettingsNotReadError from error

    def __get_key_optional(self, section: str, option: str) -> Optional[str]:
        return self.__config_parser.get(section, option, fallback=None)


class URL:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip

    @property
    def register(self) -> str:
        return f"http://{self.server_ip}/workers/register"

    @property
    def deregister(self) -> str:
        return f"http://{self.server_ip}/workers/deregister"

    @property
    def websocket(self) -> str:
        return f"ws://{self.server_ip}/workers/ws"


class DIR:
    def __init__(self, data_dir: str):
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
