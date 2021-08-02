from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import get_settings

settings = get_settings()


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app, db_url=settings.postgres_database_url, modules={"models": settings.models}
    )
