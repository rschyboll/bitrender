from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Rendering API"
    postgres_database_url: str

    class Config:
        env_file: str = "../development.env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()