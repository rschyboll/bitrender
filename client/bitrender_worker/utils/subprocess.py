"""This module contains utilities for launching and managing subprocesses."""

from asyncio import StreamReader
from asyncio.subprocess import PIPE, Process, create_subprocess_exec
from asyncio.tasks import Task, create_task
from typing import Callable, Coroutine, Optional, TypeGuard


class Subprocess:
    """Class for running subprocesses and retrieving messages from them.

    Attributes:
        returncode (int, optional): Returncode from the launched subprocess.
            Is None when the subprocess has not finished."""

    def __init__(
        self,
        launch_path: str,
        launch_args: list[str],
        on_stdout: Callable[[str], Coroutine[None, None, None]],
        on_stderr: Callable[[str], Coroutine[None, None, None]],
    ):
        """Initialize class variables.

        Args:
            launch_path (str): Path to the executable, that should be launched as a subprocess.
            launch_args (list[str]): Args that will be passed to the executable at launch.
            on_message (Callable[[SubprocessMessage], Coroutine[None, None, None]]):
                Callback that is called with messages returned from stdout and stderr streams.
        """

        self.on_stdout = on_stdout
        self.on_stderr = on_stderr
        self.returncode: Optional[int] = None
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
            self.__stderr_listener = self.__create_listener(process.stderr, MessageSource.STDERR)
        if process.stdout is not None:
            self.__stdout_listener = self.__create_listener(process.stdout, MessageSource.STDOUT)

    def __create_listener(self, stream: StreamReader, source: MessageSource) -> Task[None]:
        return create_task(self.__listen_to_stream(stream, source))

    async def __wait_for_listeners(self) -> None:
        if self.__stderr_listener is not None:
            await self.__stderr_listener
        if self.__stdout_listener is not None:
            await self.__stdout_listener

    async def __listen_to_stream(self, stream: StreamReader, source: MessageSource) -> None:
        while not stream.at_eof():
            message = self.__decode(await stream.readline())
            if self.__message_not_empty(message):
                await self.__on_message({"text": message, "source": source})

    @staticmethod
    def __message_not_empty(message: Optional[str]) -> TypeGuard[str]:
        return message is not None and not message.isspace() and message != ""

    @staticmethod
    def __decode(data: bytes) -> Optional[str]:
        try:
            return data.decode()
        except UnicodeDecodeError:
            return None