"""TODO generate docstring"""
from typing import Generic, TypeVar
from unittest.mock import AsyncMock

T = TypeVar("T")


class AwaitableMock(AsyncMock, Generic[T]):
    """TODO generate docstring"""

    def __init__(self, return_value: T, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.return_value = return_value

    def __await__(self) -> T:
        return self.return_value
