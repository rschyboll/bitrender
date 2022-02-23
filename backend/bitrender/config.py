"""Contains the system config"""
import os
from functools import lru_cache
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseSettings


class Settings(BaseSettings):
    models = ["models", "aerich.models"]
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

    def get_subtask_path(self, subtask_id: UUID) -> str:
        return os.path.join(self.subtask_dir, subtask_id.hex)

    def get_frame_path(self, frame_id: UUID) -> str:
        return os.path.join(self.frames_dir, frame_id.hex)

    def get_task_path(self, task_id: UUID) -> str:
        return os.path.join(self.task_dir, task_id.hex)


tortoise_config = {
    "connections": {"default": __settings.database_url},
    "apps": {
        "rendering_server": {
            "models": __settings.models,
            "default_connection": "default",
        },
    },
}
