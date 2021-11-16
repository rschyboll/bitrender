import os
from functools import lru_cache
from typing import Any, Dict

from pydantic import BaseSettings


class Settings(BaseSettings):
    models = [
        "models.tasks",
        "models.workers",
        "models.binaries",
        "models.subtasks",
        "models.tests",
        "models.frames",
        "aerich.models",
    ]
    database_url: str
    data_dir: str
    __task_dir: str = "tasks"

    @property
    def task_dir(self) -> str:
        return os.path.join(self.data_dir, self.__task_dir)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


__settings = get_settings()


__tortoise_config = {
    "connections": {"default": __settings.database_url},
    "apps": {
        "rendering_server": {
            "models": __settings.models,
            "default_connection": "default",
        },
    },
}


@lru_cache()
def get_tortoise_config() -> Dict[str, Any]:
    return __tortoise_config
