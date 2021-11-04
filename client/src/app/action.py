from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from asyncio import CancelledError, Task
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from aiohttp.client import ClientSession

from app.state import AppState


def _is_optional(field: type) -> bool:
    return get_origin(field) is Union[Any, Any] and type(None) in get_args(field)


def _arg_is_compatible(state: AppState, arg_key: str, arg_type: type) -> None:
    assert arg_key in state.__dict__
    if not _is_optional(arg_type):
        assert state.__dict__[arg_key] is not None
        if len(get_args(arg_type)) != 0:
            origin_type = get_origin(arg_type)
            if origin_type is not None:
                assert isinstance(state.__dict__[arg_key], origin_type)
        else:
            assert isinstance(state.__dict__[arg_key], arg_type)
    else:
        assert type(state.__dict__[arg_key]) in get_args(arg_type)


class SubtaskFailedError(Exception):
    pass


TVALUE = TypeVar("TVALUE")
TSUBVALUE = TypeVar("TSUBVALUE")


class Action(ABC, Generic[TVALUE]):
    critical: bool
    background: bool

    def __init__(self, **kwargs: Any):
        assert "state" in kwargs and isinstance(kwargs["state"], AppState)
        assert "session" in kwargs and isinstance(kwargs["session"], ClientSession)
        self.state = kwargs["state"]
        self.session = kwargs["session"]
        self.finished: List[Action[Any]] = []
        self.running: Dict[Action[Any], Task[Any]] = {}
        self.kwargs = kwargs

    @classmethod
    def create(
        cls, session: ClientSession, state: AppState, **kwargs: Any
    ) -> Action[TVALUE]:
        create_args = {"session": session, "state": state, **kwargs}
        action_args = cls.__get_args()
        for arg in action_args.items():
            _arg_is_compatible(state, arg[0], arg[1])
            create_args[arg[0]] = state.__dict__[arg[0]]
        return cls(**create_args)

    @classmethod
    def __get_args(cls) -> Dict[str, type]:
        args = get_type_hints(cls.__init__)
        args.pop("kwargs")
        return args

    async def start(self) -> TVALUE:
        try:
            try:
                value = await self._start()
                await self._cancel_background_tasks()
                return value
            except CancelledError:
                self.__cancel_tasks()
                raise
        except SubtaskFailedError:
            raise
        except Exception:
            try:
                await self._local_rollback()
            except Exception:
                pass
            raise

    @abstractmethod
    async def _start(self) -> TVALUE:
        raise NotImplementedError()

    async def _start_subaction(
        self, action_type: Type[Action[TSUBVALUE]], **kwargs: Any
    ) -> Optional[TSUBVALUE]:
        action = action_type.create(**self.kwargs, **kwargs)
        if action.background:
            self.running[action] = asyncio.create_task(action.start())
            return None
        else:
            task = asyncio.create_task(action.start())
            self.running[action] = task
            try:
                value = await task
                self.running.pop(action)
                self.finished.append(action)
                return value
            except Exception as error:
                self.__cancel_tasks()
                await self.rollback()
                raise SubtaskFailedError() from error

    async def _cancel_background_tasks(self) -> None:
        running = self.running.copy()
        for action, task in running.items():
            if action.background:
                task.cancel()
            try:
                await task
            except CancelledError:
                pass
            self.running.pop(action)
            self.finished.append(action)

    async def rollback(self) -> None:
        for action in self.running:
            await action.rollback()
        for action in self.finished:
            await action.rollback()
        await self._rollback()

    def __cancel_tasks(self) -> None:
        running = self.running.copy()
        for action, task in running.items():
            task.cancel()
            self.running.pop(action)
            self.finished.append(action)

    @abstractmethod
    async def _local_rollback(self) -> None:
        pass

    @abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError()
