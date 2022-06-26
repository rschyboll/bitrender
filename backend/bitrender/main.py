"""This module is the entry point for the app."""
import argparse
import asyncio

import uvicorn

from bitrender.data import create_admin_account
from bitrender.models import init_db, migrate


def init_deps():
    """Imports all interface implementations to allow them to be recognized by antidote"""
    # pylint: disable=unused-import,import-outside-toplevel
    import bitrender.services.helpers.deps  # noqa: F401

    # pylint: disable=unused-import,import-outside-toplevel
    import bitrender.services.user.deps  # noqa: F401


def run():
    """Runs the server."""
    # pylint: disable=import-outside-toplevel
    from .app import app

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
