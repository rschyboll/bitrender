import os
import random
import string
from typing import Generator, Type
from unittest import mock

import pytest

from config import DIR, URL, Settings
from errors.config import SettingsNotReadError, SettingsReadError, SettingsWriteError


class TestDIR:
    data_dir = "/data"

    @pytest.fixture(scope="function")
    def directories(self) -> DIR:
        return DIR(self.data_dir)

    def test_set_data_dir(self, directories: DIR) -> None:
        new_data_dir = "/test"
        assert directories.data_dir != new_data_dir
        directories.set_data_dir(new_data_dir)
        assert directories.data_dir == new_data_dir

    def test_settings_file(self, directories: DIR) -> None:
        assert directories.settings_file.startswith(self.data_dir)

    def test_download_file(self, directories: DIR) -> None:
        assert directories.download_file.startswith(self.data_dir)

    def test_binary_dir(self, directories: DIR) -> None:
        assert directories.binary_dir.startswith(self.data_dir)


class TestURL:
    server_ip = "127.0.0.1"

    @pytest.fixture(scope="function")
    def urls(self) -> URL:
        return URL(self.server_ip)

    def test_set_server_ip(self, urls: URL) -> None:
        new_server_ip = "171.0.0.1"
        assert urls.server_ip != new_server_ip
        urls.set_server_ip(new_server_ip)
        assert urls.server_ip == new_server_ip

    def test_register(self, urls: URL) -> None:
        assert self.server_ip in urls.register

    def test_deregister(self, urls: URL) -> None:
        assert self.server_ip in urls.deregister

    def test_websocket(self, urls: URL) -> None:
        assert self.server_ip in urls.websocket


class BaseTestSettings:
    settings_file = "./config_test.yml"

    @pytest.fixture(scope="function")
    def settings(self, tmpdir: str) -> Settings:
        return Settings(os.path.join(tmpdir, self.settings_file))

    @pytest.fixture(scope="function")
    def test_data(self, settings: Settings) -> dict[str, str]:
        data: dict[str, str] = {}
        for prop in settings.properties:
            data[prop] = self._get_random_string(random.randint(10, 1000))
        return data

    def _get_random_string(self, length: int) -> str:
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for _ in range(length))

    def _input_test_data(self, settings: Settings, data: dict[str, str]) -> None:
        for prop in settings.properties:
            setattr(settings, prop, data[prop])

    def _settings_equal(self, set1: Settings, set2: Settings) -> bool:
        saved = True
        for prop in set1.properties:
            if not getattr(set1, prop) == getattr(set2, prop):
                saved = False
        return saved

    def _file_exists(self, file: str) -> bool:
        return os.path.exists(file) and os.path.isfile(file)

    def _dir_exists(self, directory: str) -> bool:
        return os.path.exists(directory) and os.path.isdir(directory)

    def _get_settings_dir(self, settings: Settings) -> str:
        return os.path.abspath(os.path.dirname(settings.settings_file))

    def _remove_settings_dir(self, settings: Settings) -> None:
        settings_dir = self._get_settings_dir(settings)
        os.rmdir(settings_dir)

    def _save_raises(self, settings: Settings, error: Type[Exception]) -> bool:
        try:
            settings.save()
            return False
        except error:
            return True

    def _read_raises(self, settings: Settings, error: Type[Exception]) -> bool:
        try:
            settings.read()
            return False
        except error:
            return True

    def _saved(self, settings: Settings) -> bool:
        read_settings = Settings(settings.settings_file)
        read_settings.read()
        return self._settings_equal(settings, read_settings)

    def _create_empty_file(self, file: str) -> None:
        open(file, "a", encoding="utf-8").close()


class TestSettings(BaseTestSettings):
    def test_save(self, settings: Settings, test_data: dict[str, str]) -> None:
        assert self._save_raises(settings, SettingsWriteError)
        self._input_test_data(settings, test_data)
        assert self._file_exists(settings.settings_file) is False
        settings.save()
        assert self._file_exists(settings.settings_file)
        assert self._saved(settings)

    def test_save_no_directory(
        self, settings: Settings, test_data: dict[str, str]
    ) -> None:
        settings_dir = self._get_settings_dir(settings)
        self._input_test_data(settings, test_data)
        self._remove_settings_dir(settings)
        assert self._dir_exists(settings_dir) is False
        settings.save()
        assert self._dir_exists(settings_dir)

    def test_read(self, settings: Settings, test_data: dict[str, str]) -> None:
        assert self._read_raises(settings, SettingsReadError)
        save_settings = Settings(settings.settings_file)
        self._input_test_data(save_settings, test_data)
        save_settings.save()
        settings.read()
        self._settings_equal(settings, save_settings)

    def test_read_os_error(self, settings: Settings) -> None:
        with open(settings.settings_file, "w+", encoding="utf-8") as settings_file:
            settings_file.write("test")
        with pytest.raises(SettingsReadError):
            settings.read()

    def test_read_no_data(self, settings: Settings) -> None:
        self._create_empty_file(settings.settings_file)
        self._read_raises(settings, SettingsReadError)

    def test_delete(self, settings: Settings, test_data: dict[str, str]) -> None:
        self._input_test_data(settings, test_data)
        settings.save()
        assert self._file_exists(settings.settings_file)
        settings.read()
        settings.delete()
        assert self._file_exists(settings.settings_file) is False
        assert self._read_raises(settings, SettingsReadError)
        with pytest.raises(SettingsNotReadError):
            assert isinstance(settings.token, str)

    def test_exist(self, settings: Settings, test_data: dict[str, str]) -> None:
        self._input_test_data(settings, test_data)
        assert settings.exist() is False
        settings.save()
        assert settings.exist()

    def test_set_option(self, settings: Settings, test_data: dict[str, str]) -> None:
        self._input_test_data(settings, test_data)
        assert settings.token == test_data["token"]
        new_token = self._get_random_string(1000)
        settings.token = new_token
        assert settings.token == new_token

    def test_set_option_to_none(
        self, settings: Settings, test_data: dict[str, str]
    ) -> None:
        self._input_test_data(settings, test_data)
        assert settings.blender_version == test_data["blender_version"]
        settings.blender_version = None
        assert settings.blender_version is None

    def test_validate_settings(
        self, settings: Settings, test_data: dict[str, str]
    ) -> None:
        assert settings.validate_settings() is False
        self._input_test_data(settings, test_data)
        assert settings.validate_settings()


class TestOSErrorSettings(BaseTestSettings):
    @pytest.fixture(scope="class", autouse=True)
    def os_remove_os_error(self) -> Generator[None, None, None]:
        patcher = mock.patch("config.os.remove")
        os_error_mock = patcher.start()
        os_error_mock.side_effect = OSError
        yield
        patcher.stop()

    @pytest.fixture(scope="class", autouse=True)
    def open_os_error(self) -> Generator[None, None, None]:
        patcher = mock.patch("config.open")
        os_error_mock = patcher.start()
        os_error_mock.side_effect = OSError
        yield
        patcher.stop()

    def test_save(self, settings: Settings, test_data: dict[str, str]) -> None:
        self._input_test_data(settings, test_data)
        assert self._save_raises(settings, SettingsWriteError)

    def test_delete(self, settings: Settings, test_data: dict[str, str]) -> None:
        self._input_test_data(settings, test_data)
        self._create_empty_file(settings.settings_file)
        settings.delete()
