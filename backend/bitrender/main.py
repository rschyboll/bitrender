"""This module is the entry point for the app."""
import argparse
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from bitrender.api.role import router as role_router
from bitrender.api.user import router as user_router
from bitrender.auth.password import BCryptHelper, PasswordHelper
from bitrender.config import tortoise_config
from bitrender.data import create_admin_account
from bitrender.models import init_db, migrate

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


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
    app.include_router(user_router)
    app.include_router(role_router)
    register_tortoise(app, config=tortoise_config, add_exception_handlers=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="action")
run_parser = subparsers.add_parser("run")
init_db_parser = subparsers.add_parser("init-db")
migrate_parser = subparsers.add_parser("migrate")
create_admin_parser = subparsers.add_parser("create-admin")
create_admin_parser.add_argument("username")
create_admin_parser.add_argument("password")
create_admin_parser.add_argument("email")

args = parser.parse_args()

if __name__ == "__main__":
    if args.action == "init-db":
        asyncio.run(init_db())
    elif args.action == "migrate":
        asyncio.run(migrate())
    elif args.action == "create-admin":
        asyncio.run(create_admin_account(args.username, args.password, args.email))
    elif args.action == "run":
        run()
