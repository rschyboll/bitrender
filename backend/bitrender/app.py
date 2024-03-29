"""This module is the entry point for the app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from bitrender.api import api_router
from bitrender.api.handlers import register_library_error_handlers
from bitrender.api.handlers.role import register_role_error_handlers
from bitrender.api.handlers.user import register_user_error_handlers
from bitrender.config import tortoise_config


def init_deps() -> None:
    """Imports all interface implementations to allow them to be recognized by antidote"""
    # pylint: disable=unused-import,import-outside-toplevel
    # pylint: disable=unused-import,import-outside-toplevel
    import bitrender.services.app.deps  # noqa: F401
    import bitrender.services.helpers.deps  # noqa: F401


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:1234",
    "http://localhost:1234",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
]

init_deps()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
register_tortoise(app, config=tortoise_config)
register_user_error_handlers(app)
register_library_error_handlers(app)
register_role_error_handlers(app)
