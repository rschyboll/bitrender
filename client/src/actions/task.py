import time
import os
from asyncio import TimeoutError as AsyncioTimeout
from typing import Any, Dict, TYPE_CHECKING, Optional

from aiohttp import ClientError

from app.action import Action
from config import DIR, URL, Settings
from core.subprocess import BlenderSubprocess
from core.task import TaskStatus
from errors.connection import ConnectionException, WrongResponseException


if TYPE_CHECKING:
    from services import RPCCall
else:
    RPCCall = object


class Task(Action[None]):
    critical = True
    background = True

    def __init__(
        self,
        settings: Settings,
        tasks: Dict[str, bytes],
        rpc_call: RPCCall,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.settings = settings
        self.tasks = tasks
        self.rpc_call = rpc_call

    async def _start(self) -> None:
        print("HELLo")

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass
