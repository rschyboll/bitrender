import asyncio
import sys
from argparse import ArgumentParser, Namespace
from typing import List

from appdirs import user_data_dir  # type: ignore

from app.register import Register
from config import Config, Settings


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(prog="Rendering Client")
    subparsers = parser.add_subparsers(help="Action", dest="action", required=True)

    register_parser = subparsers.add_parser("register", help="Registers the worker")
    register_parser.add_argument("name", type=str, help="Worker name")
    register_parser.add_argument("server_ip", type=str, help="Server Ip address")

    subparsers.add_parser("run", help="Runs the worker")

    subparsers.add_parser("deregister", help="Deregister the worker")
    return parser.parse_args(args)


args_namespace = parse_args(sys.argv[1:])
action: str = args_namespace.action
data_dir = user_data_dir(Config.app_name, Config.app_author)

if action == "register":
    name: str = args_namespace.name
    server_ip: str = args_namespace.server_ip
    register_app = Register(name, server_ip, data_dir)
    asyncio.run(register_app.run())
elif action == "run":
    asyncio.run(app.run())
elif action == "deregister":
    register_app = Register(name, server_ip, data_dir)
    asyncio.run(register_app.register())
