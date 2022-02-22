"""This module contains mocks for asyncio.subprocess."""
from asyncio import Event
from typing import Any, List, Optional
from unittest.mock import AsyncMock, MagicMock


class MockStreamReader(MagicMock):
    """Mock of StreamReader from asyncio"""

    def __init__(self, values: List[bytes], *_: Any, **__: Any):
        MagicMock.__init__(self)
        self.values = values
        self.readline = AsyncMock(side_effect=self.mock_readline)
        self.at_eof = MagicMock(side_effect=self.__at_eof)

    async def mock_readline(self) -> bytes:
        """Side effect for mock readline."""
        return self.values.pop(0)

    def __at_eof(self) -> bool:
        """Side effect for mock at_eof"""
        return len(self.values) == 0


class MockProcess(MagicMock):
    """Mock of Process from asyncio.subprocess"""

    def __init__(
        self,
        *_: Any,
        returncode: Optional[int] = None,
        stdout_values: Optional[List[bytes]] = None,
        stderr_values: Optional[List[bytes]] = None,
        wait_for_terminate: bool = False,
        **__: Any
    ):
        MagicMock.__init__(self)
        self.returncode = returncode
        self.wait = AsyncMock(side_effect=self.mock_wait)
        self.stdout = self.__create_mock_stream(stdout_values)
        self.stderr = self.__create_mock_stream(stderr_values)
        self.terminate = MagicMock(side_effect=self.mock_terminate)
        self.wait_for_terminate = wait_for_terminate
        self.__event = Event()

    async def mock_wait(self) -> Optional[int]:
        """Side effect for wait mock."""
        if self.wait_for_terminate:
            await self.__event.wait()
        if self.returncode is not None:
            return self.returncode
        return None

    def mock_terminate(self) -> None:
        """Side effect for terminate mock"""
        self.__event.set()

    @staticmethod
    def __create_mock_stream(values: Optional[List[bytes]]) -> Optional[MockStreamReader]:
        if values is not None:
            return MockStreamReader(values)
        return None
