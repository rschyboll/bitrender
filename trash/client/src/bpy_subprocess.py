import sys
import os
import json
from asyncio import create_task
from asyncio.queues import PriorityQueue
from asyncio.tasks import Task
from asyncio.subprocess import Process, PIPE, create_subprocess_exec
from asyncio.futures import CancelledError
from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class ProcessMessage:
    priority: int
    message: str=field(compare=False)
    type: str=field(compare=False)

class BPYSubprocess():
    def __init__(self, python_file_path: str, **args):
        self.python_file_path: str = python_file_path
        self.args: tuple = args
        self.running: bool = False
        self.__process: Optional[Process] = None
        self.__stderr_listener: Optional[Task] = None
        self.__stdout_listener: Optional[Task] = None
        self.__queue: PriorityQueue = PriorityQueue()

    async def __aenter__(self):
        self.running = True
        self.__setup_env__()
        self.__process = await create_subprocess_exec(sys.executable, self.python_file_path, json.dumps(self.args),\
                                                    stdout=PIPE, stderr=PIPE, stdin=PIPE)
        self.__stderr_listener = create_task(self.__read_stderr__())
        self.__stdout_listener = create_task(self.__read_stdout__())

    def __setup_env__(self):
        os.environ["LANG"] = 'C'

    async def __aexit__(self, *args, **kwargs):
        self.running = False
        self.__stderr_listener.cancel()
        self.__stdout_listener.cancel()
        try:
            await self.__stderr_listener
            await self.__stdout_listener
        except CancelledError:
            pass
        try:
            self.__process.kill()
        except ProcessLookupError:
            pass
        finally:
            await self.__process.wait()

    async def __read_stdout__(self) -> str:
        stdout = None
        while stdout != b"":
            stdout: bytes = await self.__process.stdout.readline()
            stdout_str: str = stdout.decode()
            message: ProcessMessage = ProcessMessage(1, stdout_str, "stdout")
            await self.__queue.put(message)
        self.running = False

    async def __read_stderr__(self) -> str:
        stderr = None
        while stderr != b"":
            stderr: bytes = await self.__process.stderr.readline()
            stderr_str: str = stderr.decode()
            message: ProcessMessage = ProcessMessage(2, stderr_str, "stderr")
            await self.__queue.put(message)
        self.running = False

    async def receive(self) -> ProcessMessage:
        message: ProcessMessage = await self.__queue.get()
        return message
