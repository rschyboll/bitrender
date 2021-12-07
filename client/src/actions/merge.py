import os
from asyncio import TimeoutError as AsyncioTimeout
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID

from aiohttp import ClientError

from app.action import Action
from config import DIR, URL, Settings
from core.subprocess import BlenderSubprocess
from core.task import MergeTask, TaskData, TaskStatus, MergeTaskData
from errors.connection import ConnectionException, WrongResponseException

if TYPE_CHECKING:
    from services import RPCCall
else:
    RPCCall = object


class Merge(Action[None]):
    critical = True
    background = True

    def __init__(
        self,
        settings: Settings,
        urls: URL,
        rpc_call: RPCCall,
        merge_files: Dict[str, bytes],
        output_files: Dict[str, bytes],
        **kwargs: Any
    ):
        assert "merge_data" in kwargs and isinstance(
            kwargs["merge_data"], MergeTaskData
        )
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls
        self.rpc_call = rpc_call
        self.merge_data = kwargs["merge_data"]
        self.output_files = output_files
        self.merge_files = merge_files

    async def _start(self) -> None:
        await self.run_subaction(DownloadMergeFiles)
        result = await self.run_subaction(MergeFiles)
        if result and self.merge_data.composite_task_id.hex in self.output_files:
            await self.__success(self.merge_data.composite_task_id)
        else:
            await self.__error(self.merge_data.composite_task_id)
        await self.__remove_files()

    async def __success(self, composite_task_id: UUID) -> None:
        data = {
            "file": self.output_files[composite_task_id.hex],
            "composite_task_id": composite_task_id.hex,
        }
        async with self.session.post(
            self.urls.composite_task_success, data=data
        ) as response:
            if response.status == 200:
                pass

    async def __error(self, composite_task_id: UUID) -> None:
        data = {"composite_task_id": composite_task_id.hex}
        async with self.session.post(
            self.urls.composite_task_error, data=data
        ) as response:
            if response.status == 200:
                pass

    async def __remove_files(self) -> None:
        for subtask in self.merge_data.subtask_data:
            if subtask["subtask_id"].hex in self.merge_files:
                self.merge_files.pop(subtask["subtask_id"].hex)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class DownloadMergeFiles(Action[None]):
    critical = True
    background = False

    def __init__(
        self,
        urls: URL,
        settings: Settings,
        merge_files: Dict[str, bytes],
        **kwargs: Any
    ):
        assert "merge_data" in kwargs and isinstance(
            kwargs["merge_data"], MergeTaskData
        )
        super().__init__(**kwargs)
        self.merge_files = merge_files
        self.settings = settings
        self.urls = urls
        self.merge_data = kwargs["merge_data"]

    async def _start(self) -> None:
        for subtask in self.merge_data.subtask_data:
            subtask_id = subtask["subtask_id"]
            self.merge_files[subtask_id.hex] = await self._download(subtask_id)

    async def _download(self, subtask_id: UUID) -> bytes:
        try:
            async with self.session.get(self.urls.subtask(subtask_id)) as response:
                if response.status != 200:
                    raise WrongResponseException()
                return await response.content.read()
        except (ClientError, AsyncioTimeout) as error:
            raise ConnectionException() from error

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class MergeFiles(Action[bool]):
    critical = True
    background = False

    def __init__(
        self,
        directories: DIR,
        urls: URL,
        settings: Settings,
        merge_files: Dict[str, bytes],
        **kwargs: Any
    ):
        assert "merge_data" in kwargs and isinstance(
            kwargs["merge_data"], MergeTaskData
        )
        super().__init__(**kwargs)
        self.directories = directories
        self.merge_files = merge_files
        self.settings = settings
        self.urls = urls
        self.merge_data = kwargs["merge_data"]
        self.subprocess = self.__create_subprocess()
        self.status = TaskStatus()

    def __create_subprocess(self) -> BlenderSubprocess:
        return BlenderSubprocess(
            self.directories.binary,
            self.directories.merge_script,
            self.directories.blender_config_dir,
            output=os.path.join(
                self.directories.task_dir,
                self.merge_data.composite_task_id.hex + ".exr",
            ),
            merge_files=self.__parse_subtask_data(self.merge_data.subtask_data),
            files_dir=self.directories.task_dir,
        )

    def __parse_subtask_data(
        self, subtask_data: list[MergeTask]
    ) -> list[dict[str, str]]:
        new_data: list[dict[str, Any]] = []
        for data in subtask_data:
            new_data.append(
                {"samples": data["samples"], "subtask_id": data["subtask_id"].hex}
            )
        return new_data

    async def _start(self) -> bool:
        if len(self.merge_files) == 0:
            pass
        async with self.subprocess:
            while self.subprocess.running or not self.subprocess.is_empty():
                message = await self.subprocess.receive()
                if message is not None:
                    print(message.text)
                    self.status.update(message)
        if self.status.error or self.subprocess.returncode != 0:
            return False
        return True

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass
