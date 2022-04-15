"""Contains tests for BaseModel from bitrender.models.base."""
from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine, TypeVar

from tortoise.transactions import in_transaction

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")

Selector = Callable[..., Coroutine[Any, Any, T]]


class TransactionTest:
    """Helper class used for testing transactions.
    When calling it's instance, it launches two transactions in paralell.\n
    The first transaction is launched first, and it wait's for the second transaction to finish."""

    def __init__(self, select1: Selector[T1], args1: tuple, select2: Selector[T2], args2: tuple):
        """Creates an instance of the class.

        Args:
            select1 (Selector[T1]): First selector, that will keep it's transaction running,
                until the second selector finishes.
            args1 (tuple): Args that will be passed to the second selector.
            select2 (Selector[T2]): Second selector.
            args2 (tuple): Args that will be passed to the second selector"""
        self.__select1 = select1
        self.__select2 = select2
        self.__args1 = args1
        self.__args2 = args2
        self.__event_selected = asyncio.Event()
        self.__event = asyncio.Event()

    async def __call__(self) -> tuple[T1, T2]:
        """Calls the selectors in seperate transactions and returns their selected values.

        Returns:
            tuple[T1, T2]: Values of the selectors."""
        task1 = asyncio.create_task(self.__in_transaction(self.__select1, True, *self.__args1))
        task2 = asyncio.create_task(self.__in_transaction(self.__select2, False, *self.__args2))
        return (await task1, await task2)

    async def __in_transaction(self, select: Selector[T], wait: bool, *args) -> T:
        async with in_transaction():
            if not wait:
                await self.__event_selected.wait()
            entries = await select(*args)
            if wait:
                self.__event_selected.set()
                await self.__event.wait()
            else:
                self.__event.set()
            return entries
