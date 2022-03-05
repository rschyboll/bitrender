"""Contains the system config"""
import os
from functools import lru_cache
from uuid import UUID

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class containing all static launch settings for the system.

    Attributes:
        database_url (str): URL of the systems database.

    Properties:


    Returns:
        _type_: _description_
    """

    database_url: str = "postgres://postgres:@localhost/bitrender-DEV"
    data_dir: str = "/data-DEV"

    models = ["bitrender.models", "aerich.models"]

    __task_dir: str = "tasks"
    __frames_dir: str = "frames"
    __subtask_dir: str = "subtasks"

    @property
    def task_dir(self) -> str:
        """Path to the task directory. Creates it when it does not exist."""
        if not os.path.exists(self.__task_dir):
            os.mkdir(self.__task_dir)
        return self.__task_dir

    @property
    def frames_dir(self) -> str:
        """Path to the frames directory. Creates it when it does not exist."""
        path = os.path.join(self.data_dir, self.__frames_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @property
    def subtask_dir(self) -> str:
        """Path to the subtask directory. Creates it when it does not exist."""
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


@lru_cache()
def get_settings() -> Settings:
    """Allows using settings as a FastAPI dependency."""
    return Settings()


__settings = get_settings()

tortoise_config = {
    "connections": {"default": __settings.database_url},
    "apps": {
        "bitrender": {
            "models": __settings.models,
            "default_connection": "default",
        },
    },
}
