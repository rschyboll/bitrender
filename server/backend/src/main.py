"""Main application module"""
from fastapi import FastAPI

from resources import users as UserResource, add_resource_exception_handlers
from services import login as LoginService
from models import init_db

app = FastAPI()

app.include_router(UserResource.user_resources)
app.include_router(LoginService.user_services)

add_resource_exception_handlers(app)

init_db(app)
