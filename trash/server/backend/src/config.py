from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Rendering API'
    postgres_database_url: str

    token_lifetime: int = 60 * 60
    token_algorithm = 'HS256'
    token_secret_key = '17636c25f98914fcc459ede894e9c50886beb93c66587749f0275a9086ba452f'

    models = ['models.user', 'aerich.models']

    class Config:
        env_file: str = '../development.env'

@lru_cache()
def get_settings() -> Settings:
    return Settings()
