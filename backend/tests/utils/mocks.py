"""Contains utilities for mocking"""
from typing import Any, Generator, Generic, TypeVar
from unittest.mock import AsyncMock

T = TypeVar("T")


class AwaitableMock(AsyncMock, Generic[T]):
    """Class that allows creating awaitable mocks.
    The return_value passed in initialization, will be returned when awaiting that object."""

    def __init__(self, return_value: T, *args: Any, **kwargs: Any) -> None:
        """Creates an instance of the AwaitableMock class.

        Args:
            return_value (T): Value that will be returned when awaiting this object."""
        super().__init__(*args, **kwargs)
        self.return_value: T = return_value

    def __await__(self) -> Generator[None, None, T]:
        yield
        return self.return_value
