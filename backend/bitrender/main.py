"""This module is the entry point for the app."""
import argparse
import asyncio

import aerich
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from bitrender.config import tortoise_config

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


async def migrate():
    """Migrates the database based on current models."""
    command = aerich.Command(
        tortoise_config=tortoise_config,
        app="bitrender",
    )
    await command.init()
    await command.migrate()
    await command.upgrade()


async def init_db():
    """Initializes the database and populates it with initial data."""
    command = aerich.Command(
        tortoise_config=tortoise_config,
        app="bitrender",
    )
    await command.init()
    await command.init_db(True)


def run():
    """Runs the server."""
    app = FastAPI()
    register_tortoise(app, config=tortoise_config, add_exception_handlers=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--init-db", action="store_const", dest="action", const="init-db")
group.add_argument("--migrate", action="store_const", dest="action", const="migrate")
group.add_argument("--run", action="store_const", dest="action", const="run")
parser.set_defaults(action="run")

args = parser.parse_args()

if __name__ == "__main__":
    if args.action == "init-db":
        asyncio.run(init_db())
    elif args.action == "migrate":
        asyncio.run(migrate())
    elif args.action == "run":
        run()
