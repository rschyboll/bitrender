from functools import lru_cache
from pydantic import BaseSettings

tortoise_orm = {
    "connections": {"default": "postgres://postgres:@localhost/rendering_server"},
    "apps": {
        "models": {
            "models": ["models.tasks", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class Settings(BaseSettings):
    app_name = "Rendering API"
    postgres_database_url = "postgres://postgres:@localhost/rendering_server"
    postgres_test_database_url = "postgres://postgres:@localhost/test_{}"
    models = ["models.tasks", "aerich.models"]
    task_files_path = "../tasks/"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
