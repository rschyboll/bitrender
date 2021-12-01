import os
from asyncio import TimeoutError as AsyncioTimeout
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID

from aiohttp import ClientError

from app.action import Action
from config import DIR, URL, Settings
from core.subprocess import BlenderSubprocess
from core.task import TaskData, TaskStatus
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
        urls: URL,
        tasks: Dict[str, bytes],
        output_files: Dict[str, bytes],
        rpc_call: RPCCall,
        **kwargs: Any
    ):
        assert "task_data" in kwargs and isinstance(kwargs["task_data"], TaskData)
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls
        self.tasks = tasks
        self.output_files = output_files
        self.rpc_call = rpc_call
        self.task_data = kwargs["task_data"]

    async def _start(self) -> None:
        if not self.task_data.subtask_id.hex in self.tasks:
            await self.run_subaction(DownloadTask)
        samples = await self.run_subaction(RenderTestTask)
        if (
            self.task_data.subtask_id.hex in self.output_files
            and self.output_files[self.task_data.subtask_id.hex] != b""
            and samples is not None
        ):
            await self.__success(self.task_data.subtask_id, samples)
        else:
            await self.__error(self.task_data.subtask_id)
        await self.__remove_task()

    async def __success(self, subtask_id: UUID, samples: int) -> None:
        data = {
            "file": self.output_files[subtask_id.hex],
            "subtask_id": subtask_id.hex,
            "samples": str(samples),
        }
        async with self.session.post(self.urls.subtask_success, data=data) as response:
            if response.status == 200:
                pass

    async def __error(self, subtask_id: UUID) -> None:
        data = {"subtask_id": subtask_id.hex}
        async with self.session.post(self.urls.subtask_error, data=data) as response:
            if response.status == 200:
                pass

    async def __remove_task(self) -> None:
        if self.task_data.task_id.hex in self.tasks:
            self.tasks.pop(self.task_data.task_id.hex)
        if self.task_data.subtask_id.hex in self.output_files:
            self.output_files.pop(self.task_data.subtask_id.hex)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class DownloadTask(Action[None]):
    critical = True
    background = False

    def __init__(
        self, urls: URL, settings: Settings, tasks: Dict[str, bytes], **kwargs: Any
    ):
        assert "task_data" in kwargs and isinstance(kwargs["task_data"], TaskData)
        super().__init__(**kwargs)
        self.settings = settings
        self.tasks = tasks
        self.urls = urls
        self.task_data = kwargs["task_data"]

    async def _start(self) -> None:
        self.tasks[self.task_data.task_id.hex] = await self.__download(
            self.task_data.task_id
        )

    async def __download(self, task_id: UUID) -> bytes:
        try:
            async with self.session.get(self.urls.task(task_id)) as response:
                if response.status != 200:
                    raise WrongResponseException()
                return await response.content.read()
        except (ClientError, AsyncioTimeout) as error:
            raise ConnectionException() from error

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class RenderTestTask(Action[Optional[int]]):
    critical = True
    background = False

    def __init__(self, directories: DIR, rpc_call: RPCCall, **kwargs: Any):
        super().__init__(**kwargs)
        assert "task_data" in kwargs and isinstance(kwargs["task_data"], TaskData)
        self.directories = directories
        self.rpc_call = rpc_call
        self.status = TaskStatus()
        self.task_data = kwargs["task_data"]
        self.subprocess = self.__create_subprocess()

    def __create_subprocess(self) -> BlenderSubprocess:
        return BlenderSubprocess(
            self.directories.binary,
            self.directories.render_script,
            self.directories.blender_config_dir,
            task=os.path.join(self.directories.task_dir, self.task_data.task_id.hex),
            samples=self.task_data.max_samples,
            offset=self.task_data.samples_offset,
            res_x=self.task_data.resolution_x,
            res_y=self.task_data.resolution_y,
            time_limit=self.task_data.time_limit,
            output=os.path.join(
                self.directories.task_dir, self.task_data.subtask_id.hex + ".exr"
            ),
        )

    async def _start(self) -> Optional[int]:
        async with self.subprocess:
            while self.subprocess.running or not self.subprocess.is_empty():
                message = await self.subprocess.receive()
                if message is not None:
                    print(message.text)
                    self.status.update(message)
        if self.status.error or self.subprocess.returncode != 0:
            return None
        return self.status.samples

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass
