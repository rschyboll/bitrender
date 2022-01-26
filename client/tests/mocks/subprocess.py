"""This module contains functions for creating mocks for subprocess calls."""
from typing import List, Optional
from unittest.mock import AsyncMock, MagicMock

from black import asyncio
from pytest_mock import MockerFixture


class MockStreamReader(MagicMock):
    def __init__(self, values: List[bytes]):
        MagicMock.__init__(self)
        self.values = values

    async def readline(self) -> bytes:
        return self.values.pop(0)

    def at_eof(self) -> bool:
        return len(self.values) == 0


class MockProcess(MagicMock):
    def __init__(
        self,
        returncode: int = 0,
        stdout_values: Optional[List[bytes]] = None,
        stderr_values: Optional[List[bytes]] = None,
    ):
        MagicMock.__init__(self)
        self.returncode = returncode
        self.stdout: Optional[MockStreamReader] = None
        if stdout_values is not None:
            self.stdout = MockStreamReader(stdout_values.copy())
        self.stderr: Optional[MockStreamReader] = None
        if stderr_values is not None:
            self.stderr = MockStreamReader(stderr_values.copy())
        self.terminate = AsyncMock()

    async def wait(self) -> int:
        await asyncio.sleep(self.timeout)
        return self.returncode


def mock_create_subprocess_exec(mocker: MockerFixture, return_value: MockProcess) -> MagicMock:
    """Creates a create_subprocess_exec mock and assigns a return_value to it.

    Args:
        mocker (MockerFixture): Mocker fixture from pytest-mock library.
        return_value (Any): Value that should be returned when calling create_subprocess_exec.

    Returns:
        MagicMock: Mocked create_subprocess_exec"""
    mock = mocker.patch("bitrender_worker.utils.subprocess.create_subprocess_exec")
    mock.return_value = return_value

    return mock
