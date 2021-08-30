import json
import os
from typing import Any, Optional, Tuple

import aiofiles
from appdirs import user_data_dir  # type: ignore

from config import Config, Settings
from errors.settings import SettingsLoadError, SettingsWriteError

data_dir = user_data_dir(Config.app_name, Config.app_author)
settings_file = os.path.join(data_dir, Config.settings_file)


def settings_exist() -> bool:
    try:
        return os.path.exists(settings_file)
    except (OSError, IOError):
        return False


async def save_settings(settings: Settings) -> None:
    try:
        data = settings._asdict()
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        async with aiofiles.open(settings_file, mode="w+") as file:
            await file.write(json.dumps(data))
    except (OSError, IOError) as error:
        raise SettingsWriteError() from error


async def load_settings() -> Settings:
    try:
        async with aiofiles.open(settings_file, "r") as file:
            data = await file.read()
            data_dict: dict[str, Any] = json.loads(data)
            return Settings(**data_dict)
    except (OSError, IOError, TypeError) as error:
        raise SettingsLoadError() from error


version_file = os.path.join(data_dir, Config.version_file)


async def save_current_version(version: str, url: str) -> None:
    try:
        if not os.path.exists(version_file):
            os.mkdir(version_file)
        async with aiofiles.open(version_file, mode="w+") as file:
            await file.write(version)
    except (OSError, IOError) as error:
        raise SettingsWriteError() from error


async def load_current_version() -> Optional[Tuple[str, str]]:
    try:
        async with aiofiles.open(settings_file, "r") as file:
            data = await file.read()
            return data
    except (OSError, IOError):
        return None


def remove_settings() -> None:
    if settings_exist():
        os.remove(settings_file)
