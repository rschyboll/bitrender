"""Main application module"""
from fastapi import FastAPI
from models import init_db
from resources import add_resource_exception_handlers
from resources import users as UserResource
from services import login as LoginService

app = FastAPI()

app.include_router(UserResource.user_resources)
app.include_router(LoginService.user_services)

add_resource_exception_handlers(app)

init_db(app)
