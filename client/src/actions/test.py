import os
import time
from asyncio import TimeoutError as AsyncioTimeout
from typing import TYPE_CHECKING, Any, Dict, Optional

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
        if "test" not in self.tasks:
            await self.run_subaction(DownloadTestTask)
        await self.__render_test(1)
        sync_time = await self.__render_test(1)
        render_time = await self.__render_test()
        if sync_time is not None and render_time is not None:
            await self.rpc_call.test_success(sync_time, render_time)
        else:
            await self.rpc_call.test_error()
        self.tasks.pop("test")

    async def __render_test(self, samples: Optional[int] = None) -> Optional[float]:
        return await self.run_subaction(RenderTestTask, samples=samples)

    async def _local_rollback(self) -> None:
        await self.rpc_call.test_error()

    async def _rollback(self) -> None:
        pass


class RenderTestTask(Action[Optional[float]]):
    critical = True
    background = False

    def __init__(self, directories: DIR, rpc_call: RPCCall, **kwargs: Any):
        super().__init__(**kwargs)
        assert "samples" in kwargs
        self.directories = directories
        self.rpc_call = rpc_call
        self.samples = kwargs["samples"]
        self.status = TaskStatus()
        self.subprocess = self.__create_subprocess()

    def __create_subprocess(self) -> BlenderSubprocess:
        return BlenderSubprocess(
            self.directories.binary,
            self.directories.render_script,
            self.directories.blender_config_dir,
            task=os.path.join(self.directories.task_dir, "test"),
            samples=self.samples,
        )

    async def _start(self) -> Optional[float]:
        start = time.time()
        async with self.subprocess:
            while self.subprocess.running or not self.subprocess.is_empty():
                message = await self.subprocess.receive()
                if message is not None:
                    self.status.update(message)
        if self.status.error or self.subprocess.returncode != 0:
            return None
        end = time.time()
        return end - start

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
