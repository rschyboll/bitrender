import os
from asyncio import TimeoutError as AsyncioTimeout
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID

from aiohttp import ClientError

from app.action import Action
from config import DIR, URL, Settings
from core.subprocess import BlenderSubprocess
from core.task import TaskData, TaskStatus, MergeTaskData
from errors.connection import ConnectionException, WrongResponseException

if TYPE_CHECKING:
    from services import RPCCall
else:
    RPCCall = object


class Merge(Action[None]):
    critical = True
    background = True

    def __init__(self, settings: Settings, urls: URL, rpc_call: RPCCall, **kwargs: Any):
        assert "merge_data" in kwargs and isinstance(
            kwargs["merge_data"], MergeTaskData
        )
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls
        self.rpc_call = rpc_call
        self.merge_data = kwargs["merge_data"]

    async def _start(self) -> None:
        pass

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class DownloadMergeFiles(Action[None]):
    critical = True
    background = False

    def __init__(
        self, urls: URL, settings: Settings, tasks: Dict[str, bytes], **kwargs: Any
    ):
        assert "merge_data" in kwargs and isinstance(kwargs["merge_data"], MergeData)
        super().__init__(**kwargs)
        self.settings = settings
        self.tasks = tasks
        self.urls = urls
        self.merge_data = kwargs["merge_data"]

    async def _start(self) -> None:
        pass

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass
