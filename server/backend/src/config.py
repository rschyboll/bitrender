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
        "models.composite_tasks",
        "models.subtasks_assignments",
        "models.composite_assignments",
        "aerich.models",
    ]
    database_url: str
    data_dir: str
    __task_dir: str = "tasks"
    __frames_dir: str = "frames"
    __subtask_dir: str = "subtasks"
    test_time = 60
    task_time = 60 * 5
    safe_time = 60 * 10

    @property
    def task_dir(self) -> str:
        path = os.path.join(self.data_dir, self.__task_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @property
    def frames_dir(self) -> str:
        path = os.path.join(self.data_dir, self.__frames_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @property
    def subtask_dir(self) -> str:
        path = os.path.join(self.data_dir, self.__subtask_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path


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
