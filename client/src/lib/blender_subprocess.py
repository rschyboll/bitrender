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
    message: str = field(compare=False)
    type: MessageType = field(compare=False)


class BlenderSubprocess:
    def __init__(
        self,
        blender_bin_path: str,
        script_path: str,
        config_path: str,
        **kwargs: dict[str, Any]
    ) -> None:
        self.blender_bin_path: str = blender_bin_path
        self.script_path: str = script_path
        self.config_path: str = config_path
        self.kwargs: dict[str, Any] = kwargs
        self.__process: Optional[Process] = None
        self.__stderr_listener: Optional[Task] = None
        self.__stdout_listener: Optional[Task] = None
        self.__queue: PriorityQueue[ProcessMessage] = PriorityQueue()
        self.running: bool = False

    async def __aenter__(self):
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

    def __setup_env__(self):
        os.environ["LANG"] = "C"
        os.environ["BLENDER_USER_CONFIG"] = self.config_path

    def __start_listeners(self):
        self.__stdout_listener = create_task(self.__read_stdout__())
        self.__stderr_listener = create_task(self.__read_stderr__())

    async def __aexit__(self, *args, **kwargs):
        self.running = False
        await self.__stop_listeners()
        try:
            self.__process.kill()
        except ProcessLookupError:
            pass
        finally:
            await self.__process.wait()

    async def __stop_listeners(self):
        self.__stderr_listener.cancel()
        self.__stdout_listener.cancel()
        try:
            await self.__stderr_listener
        except CancelledError:
            pass
        try:
            await self.__stdout_listener
        except CancelledError:
            pass

    async def __read_stdout__(self):
        stdout = None
        while stdout != b"":
            stdout = await self.__process.stdout.readline()
            stdout_str = self.__decode_bytes(stdout)
            if stdout_str is None:
                message = ProcessMessage(
                    MessagePriority.STDOUT, "Decode error", MessageType.STDOUT
                )
            else:
                message = ProcessMessage(
                    MessagePriority.STDOUT, stdout_str, MessageType.STDOUT
                )
            await self.__queue.put(message)
        message = ProcessMessage(MessagePriority.STATE, "stdout end", MessageType.STATE)
        await self.__queue.put(message)
        self.running = False

    async def __read_stderr__(self):
        stderr = None
        while stderr != b"":
            stderr = await self.__process.stderr.readline()
            stderr_str = self.__decode_bytes(stderr)
            if stderr_str is None:
                message = ProcessMessage(
                    MessagePriority.STATE, "Decode error", MessageType.STATE
                )
            else:
                message = ProcessMessage(
                    MessagePriority.STDERR, stderr_str, MessageType.STDERR
                )
            await self.__queue.put(message)
        message = ProcessMessage(MessagePriority.STATE, "stderr end", MessageType.STATE)
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

    async def receive(self) -> ProcessMessage:
        message = await self.__queue.get()
        return message
