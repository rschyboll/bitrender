from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Rendering API"
    postgres_database_url: str
    registration_token_lifetime: int = 60 * 60
    token_algorithm = 'HS256'

    models = ['models.user', 'aerich.models']

    class Config:
        env_file: str = "../development.env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
