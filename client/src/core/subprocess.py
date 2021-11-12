import asyncio
import json
import os
from asyncio import CancelledError
from asyncio.queues import PriorityQueue
from asyncio.subprocess import PIPE, Process, create_subprocess_exec
from asyncio.tasks import Task, create_task
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Optional


class MessagePriority(IntEnum):
    STDOUT = 1
    STDERR = 2
    STATE = 3


class MessageType(Enum):
    STDERR = "stderr"
    STDOUT = "stdout"
    STATE = "state"


@dataclass(order=True)
class ProcessMessage:
    priority: MessagePriority
    text: str = field(compare=False)
    type: MessageType = field(compare=False)


class BlenderSubprocess:
    def __init__(
        self, blender_bin_path: str, script_path: str, config_path: str, **kwargs: Any
    ) -> None:
        self.blender_bin_path = blender_bin_path
        self.script_path = script_path
        self.config_path = config_path
        self.kwargs = kwargs
        self.__process: Optional[Process] = None
        self.__stderr_listener: Optional[Task[None]] = None
        self.__stdout_listener: Optional[Task[None]] = None
        self.__queue: PriorityQueue[ProcessMessage] = PriorityQueue()
        self.running: bool = False
        self.returncode: Optional[int] = None

    async def __aenter__(self) -> None:
        self.running = True
        self.__setup_env__()
        self.__process = await create_subprocess_exec(
            self.blender_bin_path,
            "-b",
            "--python",
            self.script_path,
            "--",
            json.dumps(self.kwargs),
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
        )
        self.__start_listeners()

    def __setup_env__(self) -> None:
        os.environ["LANG"] = "C"
        os.environ["BLENDER_USER_CONFIG"] = self.config_path

    def __start_listeners(self) -> None:
        self.__stdout_listener = create_task(self.__read_stdout__())
        self.__stderr_listener = create_task(self.__read_stderr__())

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        self.running = False
        await self.__stop_listeners()
        if self.__process is not None:
            try:
                self.__process.kill()
            except ProcessLookupError:
                pass
            await self.__process.wait()
            self.returncode = self.__process.returncode

    async def __stop_listeners(self) -> None:
        if self.__stderr_listener is not None:
            self.__stderr_listener.cancel()
            try:
                await self.__stderr_listener
            except CancelledError:
                pass
        if self.__stdout_listener is not None:
            self.__stdout_listener.cancel()
            try:
                await self.__stdout_listener
            except CancelledError:
                pass

    async def __read_stdout__(self) -> None:
        if self.__process is not None and self.__process.stdout is not None:
            while not self.__process.stdout.at_eof():
                stdout = await self.__process.stdout.readline()
                stdout_str = self.__decode_bytes(stdout)
                if (
                    stdout_str is not None
                    and not stdout_str.isspace()
                    and stdout_str != ""
                ):
                    message = ProcessMessage(
                        MessagePriority.STDOUT, stdout_str, MessageType.STDOUT
                    )
                    await self.__queue.put(message)
        self.running = False

    async def __read_stderr__(self) -> None:
        if self.__process is not None and self.__process.stderr is not None:
            while not self.__process.stderr.at_eof():
                stderr = await self.__process.stderr.readline()
                stderr_str = self.__decode_bytes(stderr)
                if (
                    stderr_str is not None
                    and not stderr_str.isspace()
                    and stderr_str != ""
                ):
                    message = ProcessMessage(
                        MessagePriority.STDERR, stderr_str, MessageType.STDERR
                    )
                    await self.__queue.put(message)
        self.running = False

    def __decode_bytes(self, data: bytes) -> Optional[str]:
        try:
            data_str = data.decode()
            return data_str
        except UnicodeDecodeError:
            return None

    def is_empty(self) -> bool:
        return self.__queue.empty()

    async def receive(self) -> Optional[ProcessMessage]:
        if self.is_empty():
            await asyncio.sleep(0.01)
            return None
        message = await self.__queue.get()
        return message
