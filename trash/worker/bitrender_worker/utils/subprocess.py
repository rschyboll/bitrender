"""This module contains utilities for launching and managing subprocesses."""

from asyncio import StreamReader
from asyncio.subprocess import PIPE, Process, create_subprocess_exec
from asyncio.tasks import Task, create_task
from typing import Callable, Coroutine, Optional, TypeGuard

StreamCallback = Callable[[str], Coroutine[None, None, None]]


class Subprocess:
    """Class for running subprocesses and retrieving messages from them.

    Attributes:
        returncode (int, optional): Returncode from the launched subprocess.
            Is None when the subprocess has not finished."""

    def __init__(
        self,
        launch_path: str,
        launch_args: list[str],
        on_stdout: StreamCallback,
        on_stderr: StreamCallback,
    ):
        """Args:
        launch_path (str): Path to the executable, that should be launched as a subprocess.
        launch_args (list[str]): Args that will be passed to the executable at launch.
        on_stdout (StreamCallback): Callback that is called with messages from stdout stream.
        on_stderr (StreamCallback): Callback that is called with messages from stderr stream."""
        self.returncode: Optional[int] = None
        self.__on_stdout = on_stdout
        self.__on_stderr = on_stderr
        self.__launch_path = launch_path
        self.__launch_args = launch_args
        self.__process: Optional[Process] = None
        self.__stdout_listener: Optional[Task[None]] = None
        self.__stderr_listener: Optional[Task[None]] = None

    async def run(self) -> int:
        """Launches the subprocess, starts listening to its streams, and waits until it finishes.

        Returns:
            int: return code from the launched subprocess."""
        self.__process = await self.__create()
        self.__start_listeners(self.__process)

        self.returncode = await self.__process.wait()
        await self.__wait_for_listeners()

        return self.returncode

    async def stop(self) -> None:
        """Stops the running subprocess and the listeners."""
        if self.__process is not None and self.__process.returncode is None:
            self.__process.terminate()
            self.returncode = await self.__process.wait()
        await self.__wait_for_listeners()

    async def __create(self) -> Process:
        return await create_subprocess_exec(
            self.__launch_path, *self.__launch_args, stdout=PIPE, stderr=PIPE
        )

    def __start_listeners(self, process: Process) -> None:
        if process.stderr is not None:
            self.__stderr_listener = self.__create_listener(process.stderr, self.__on_stderr)
        if process.stdout is not None:
            self.__stdout_listener = self.__create_listener(process.stdout, self.__on_stdout)

    def __create_listener(self, stream: StreamReader, on_message: StreamCallback) -> Task[None]:
        return create_task(self.__listen_to_stream(stream, on_message))

    async def __wait_for_listeners(self) -> None:
        if self.__stderr_listener is not None:
            await self.__stderr_listener
        if self.__stdout_listener is not None:
            await self.__stdout_listener

    async def __listen_to_stream(self, stream: StreamReader, on_message: StreamCallback) -> None:
        while not stream.at_eof():
            message = self.__decode(await stream.readline())
            if self.__message_not_empty(message):
                await on_message(message)

    @staticmethod
    def __message_not_empty(message: Optional[str]) -> TypeGuard[str]:
        return message is not None and not message.isspace() and message != ""

    @staticmethod
    def __decode(data: bytes) -> Optional[str]:
        try:
            return data.decode()
        except UnicodeDecodeError:
            return None
