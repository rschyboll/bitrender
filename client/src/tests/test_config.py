import os
import random
import string

import pytest
from unittest import mock
from configparser import ConfigParser

from config import DIR, URL, Settings
from errors.settings import SettingsNotReadError, SettingsReadError, SettingsWriteError


class TestDIR:
    data_dir = "/data"

    @pytest.fixture(scope="class")
    def directories(self) -> DIR:
        return DIR(self.data_dir)

    def test_settings_file(self, directories: DIR) -> None:
        assert directories.settings_file.startswith(self.data_dir)

    def test_download_file(self, directories: DIR) -> None:
        assert directories.download_file.startswith(self.data_dir)

    def test_binary_dir(self, directories: DIR) -> None:
        assert directories.binary_dir.startswith(self.data_dir)


class TestURL:
    server_ip = "/data"

    @pytest.fixture(scope="class")
    def urls(self) -> URL:
        return URL(self.server_ip)

    def test_register(self, urls: URL) -> None:
        assert self.server_ip in urls.register

    def test_deregister(self, urls: URL) -> None:
        assert self.server_ip in urls.deregister

    def test_websocket(self, urls: URL) -> None:
        assert self.server_ip in urls.websocket


SettingsData = tuple[str, str, str, str]


class TestSettings:
    settings_file = "./config_test.yml"

    @pytest.fixture(scope="function")
    def settings(self, tmpdir: str) -> Settings:
        return Settings(os.path.join(tmpdir, self.settings_file))

    @pytest.fixture(scope="function")
    def data(self) -> SettingsData:
        return (
            self.__get_random_string(random.randint(0, 100)),
            self.__get_random_string(random.randint(0, 100)),
            self.__get_random_string(random.randint(0, 100)),
            self.__get_random_string(random.randint(0, 100)),
        )

    def test_save(self, settings: Settings, data: SettingsData) -> None:
        with pytest.raises(SettingsWriteError):
            settings.save()

        self.__input_data(settings, data)
        assert os.path.exists(settings.settings_file) is False

        settings.save()
        assert os.path.exists(settings.settings_file)

        read_settings = Settings(settings.settings_file)
        read_settings.read()
        self.__compare_settings_objects(settings, read_settings)

    def test_save_os_error(self, settings: Settings, data: SettingsData) -> None:
        self.__input_data(settings, data)
        with mock.patch("config.open") as mock_open:
            mock_open.side_effect = OSError
            with pytest.raises(SettingsWriteError):
                settings.save()

    def test_read(self, settings: Settings, data: SettingsData) -> None:
        with pytest.raises(SettingsReadError):
            settings.read()
        save_settings = Settings(settings.settings_file)
        self.__input_data(save_settings, data)
        save_settings.save()
        settings.read()
        self.__compare_settings_objects(settings, save_settings)

    def test_read_os_error(self, settings: Settings) -> None:
        with open(settings.settings_file, "w+", encoding="utf-8") as settings_file:
            settings_file.write("test")
        with pytest.raises(SettingsReadError):
            settings.read()

    def test_read_no_data(self, settings: Settings) -> None:
        open(settings.settings_file, "a", encoding="utf-8").close()
        with pytest.raises(SettingsReadError):
            settings.read()

    def test_delete(self, settings: Settings, data: SettingsData) -> None:
        self.__input_data(settings, data)
        settings.save()
        assert os.path.exists(settings.settings_file)
        settings.read()
        settings.delete()
        assert os.path.exists(settings.settings_file) is False
        with pytest.raises(SettingsReadError):
            settings.read()
        with pytest.raises(SettingsNotReadError):
            assert isinstance(settings.token, str)
        open(settings.settings_file, "a", encoding="utf-8").close()
        with mock.patch("os.remove") as mock_open:
            mock_open.side_effect = OSError
            settings.delete()

    def test_exist(self, settings: Settings, data: SettingsData) -> None:
        self.__input_data(settings, data)
        assert settings.exist() is False
        settings.save()
        assert settings.exist()

    def test_validate_settings(self, settings: Settings, data: SettingsData) -> None:
        assert settings.validate_settings() is False
        self.__input_data(settings, data)
        assert settings.validate_settings()

    def __compare_settings_objects(
        self, settings_1: Settings, settings_2: Settings
    ) -> None:
        assert settings_1.token == settings_2.token
        assert settings_1.name == settings_2.name
        assert settings_1.server_ip == settings_2.server_ip
        assert settings_1.blender_version == settings_2.blender_version

    def __input_data(self, settings: Settings, data: SettingsData) -> None:
        settings.token = data[0]
        settings.name = data[1]
        settings.server_ip = data[2]
        settings.blender_version = data[3]

    def __get_random_string(self, length: int) -> str:
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(length))
