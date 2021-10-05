import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Optional, Tuple

import aiofiles
from appdirs import user_data_dir  # type: ignore

from config import Config, Settings
from errors.settings import SettingsLoadError, SettingsWriteError

data_dir = user_data_dir(Config.app_name, Config.app_author)
settings_file = os.path.join(data_dir, Config.settings_file)
version_file = os.path.join(data_dir, Config.version_file)
temp_file_path = os.path.join(data_dir, "blender.tar.xz")
binary_dir = os.path.join(data_dir, Config.binary_dir)


def settings_exist() -> bool:
    try:
        return os.path.exists(settings_file)
    except OSError:
        return False


async def save_settings(settings: Settings) -> None:
    try:
        data = settings._asdict()
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        async with aiofiles.open(settings_file, mode="w+") as file:
            await file.write(json.dumps(data))
    except (OSError, TypeError, ValueError) as error:
        rollback_save_settings()
        raise SettingsWriteError() from error


def rollback_save_settings() -> None:
    try:
        if os.path.exists(settings_file):
            os.remove(settings_file)
    except OSError:
        return


async def load_settings() -> Settings:
    try:
        async with aiofiles.open(settings_file, "r") as file:
            data = await file.read()
            data_dict: dict[str, Any] = json.loads(data)
            return Settings(**data_dict)
    except (OSError, TypeError, ValueError, JSONDecodeError) as error:
        rollback_save_settings()
        raise SettingsLoadError() from error


async def save_current_version(version: str, url: str) -> None:
    try:
        data = {"version": version, "url": url}
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        async with aiofiles.open(version_file, mode="w+") as file:
            await file.write(json.dumps(data))
    except (OSError, TypeError, ValueError, JSONDecodeError) as error:
        rollback_save_current_version()
        raise SettingsWriteError() from error


def rollback_save_current_version() -> None:
    try:
        if os.path.exists(version_file):
            os.remove(version_file)
    except OSError:
        return


async def load_current_version() -> Optional[Tuple[str, str]]:
    try:
        async with aiofiles.open(version_file, "r") as file:
            data = await file.read()
            decoded_data = json.loads(data)
            return decoded_data["version"], decoded_data["url"]
    except (OSError, TypeError, JSONDecodeError):
        rollback_save_current_version()
        return None


def remove_settings() -> None:
    try:
        if os.path.exists(settings_file):
            os.remove(settings_file)
    except OSError:
        return
