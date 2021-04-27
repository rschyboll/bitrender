"""Module containing user ORM model"""
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.models import Model
from tortoise.fields.data import IntField

from config import get_settings

settings = get_settings()

TORTOISE_ORM = {
    "connections": {"default": settings.postgres_database_url},
    "apps": {
        "models": {
            "models": settings.models,
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI) -> None:
    register_tortoise(
    app,
    db_url=settings.postgres_database_url,
    modules={"models": settings.models}
)

class BaseModel(Model):
    id = IntField(pk = True)

    class Meta:
        abstract = True