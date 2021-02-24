"""Main application module"""
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import get_settings
from resources import users as UserResource
from services import users as UserService

app = FastAPI()
settings = get_settings()

app.include_router(UserResource.user_resources)
app.include_router(UserService.user_services)

register_tortoise(
    app,
    db_url=settings.postgres_database_url,
    modules={"models": ["models.user"]}
)
