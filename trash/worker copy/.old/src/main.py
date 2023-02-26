import asyncio
import sys
import traceback
from argparse import ArgumentParser, Namespace
from typing import Any, List, Type

from actions.binary import UpdateBinary
from actions.config import GetRegisterConfig, GetWorkerConfig
from actions.fuse import Fuse
from actions.register import DeregisterWorker, RegisterWorker
from actions.rpc import RPC
from app.action import Action
from app.app import App


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

actions: List[Type[Action[Any]]] = []

loop = asyncio.get_event_loop()
try:
    if action == "register":
        name: str = args_namespace.name
        server_ip: str = args_namespace.server_ip
        actions = [GetRegisterConfig, RegisterWorker]
        app = App(actions, name=name, server_ip=server_ip)
    elif action == "run":
        actions = [GetWorkerConfig, Fuse, UpdateBinary, RPC]
        app = App(actions)
    elif action == "deregister":
        actions = [GetWorkerConfig, DeregisterWorker]
        app = App(actions)
    loop.run_until_complete(app.run())
except KeyboardInterrupt:
    loop.run_until_complete(app.cleanup())
except Exception as error:
    loop.run_until_complete(app.cleanup())
    traceback.print_exc()
