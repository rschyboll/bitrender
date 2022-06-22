"""This module is the entry point for the app."""
import argparse
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware
from tortoise.contrib.fastapi import register_tortoise

from bitrender.api import api_router
from bitrender.api.handlers import register_library_error_handlers
from bitrender.api.handlers.auth import register_auth_error_handlers
from bitrender.config import tortoise_config
from bitrender.data import create_admin_account
from bitrender.models import init_db, migrate

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


def init_deps():
    """Imports all interface implementations to allow them to be recognized by antidote"""
    import bitrender.services.user.deps  # noqa: F401 # pylint: disable=unused-import
    import bitrender.services.utils.deps  # noqa: F401 # pylint: disable=unused-import


def run():
    """Runs the server."""
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    app.add_middleware(RawContextMiddleware)
    register_tortoise(app, config=tortoise_config)
    register_auth_error_handlers(app)
    register_library_error_handlers(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="action")
run_parser = subparsers.add_parser("run")
init_db_parser = subparsers.add_parser("init-db")
migrate_parser = subparsers.add_parser("migrate")
create_admin_parser = subparsers.add_parser("create-admin")
create_admin_parser.add_argument("password")
create_admin_parser.add_argument("email")

args = parser.parse_args()

if __name__ == "__main__":
    if args.action == "init-db":
        asyncio.run(init_db())
    elif args.action == "migrate":
        asyncio.run(migrate())
    elif args.action == "create-admin":
        asyncio.run(create_admin_account(args.password, args.email))
    elif args.action == "run":
        run()
