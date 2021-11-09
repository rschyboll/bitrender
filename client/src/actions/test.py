import asyncio
import os
from asyncio import TimeoutError as AsyncioTimeout
from typing import Any, Dict, List, TYPE_CHECKING

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


class Test(Action[None]):
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
        return
        if "test" not in self.tasks:
            await self.start_subaction(DownloadTestTask)
        await asyncio.sleep(2)
        await self.start_subaction(RenderTestTask)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class RenderTestTask(Action[int]):
    critical = True
    background = False

    def __init__(self, tasks: Dict[str, bytes], directories: DIR, **kwargs: Any):
        super().__init__(**kwargs)
        assert "rpc_call" in kwargs and isinstance(kwargs["rpc_call"], RPCCall)
        self.messages: List[str] = []
        self.tasks = tasks
        self.directories = directories
        self.rpc_call = kwargs["rpc_call"]
        self.status = TaskStatus()
        self.subprocess = BlenderSubprocess(
            directories.binary,
            os.path.join(directories.render_scripts_dir, "test.py"),
            directories.blender_config_dir,
            task=os.path.join(directories.task_dir, "test2"),
        )

    async def _start(self) -> int:
        async with self.subprocess:
            while self.subprocess.running or not self.subprocess.is_empty():
                message = await self.subprocess.receive()
                self.status.update(message)
                print(message.priority, end=" ")
                print(message.text)
        print(self.status.finished)
        print(self.subprocess.returncode)
        return 1

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class DownloadTestTask(Action[None]):
    critical = True
    background = False

    def __init__(self, urls: URL, tasks: Dict[str, bytes], **kwargs: Any):
        super().__init__(**kwargs)
        self.tasks = tasks
        self.urls = urls

    async def _start(self) -> None:
        task = await self.__download()
        self.tasks["test"] = task

    async def __download(self) -> bytes:
        try:
            async with self.session.get(self.urls.test_task) as response:
                if response.status != 200:
                    raise WrongResponseException()
                return await response.content.read()
        except (ClientError, AsyncioTimeout) as error:
            raise ConnectionException() from error

    async def _local_rollback(self) -> None:
        if "test" in self.tasks:
            self.tasks.pop("test")

    async def _rollback(self) -> None:
        pass
