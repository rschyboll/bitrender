import asyncio
import traceback
from asyncio import CancelledError, Task
from typing import Any, Dict, List, Type

from aiohttp.client import ClientSession, ClientTimeout

from actions.log import Logger
from app.action import Action
from app.state import AppState
from errors import UserError


class App:
    def __init__(self, action_types: List[Type[Action[Any]]], **kwargs: Any):
        self.state = AppState()
        self.action_types = action_types
        self.kwargs = kwargs
        self.finished: List[Action[Any]] = []
        self.running: Dict[Action[Any], Task[None]] = {}
        self.logger = Logger(self.running, self.finished)

    async def run(self) -> None:
        async with ClientSession() as session:
            try:
                logger = asyncio.create_task(self.logger.start())
                for action_type in self.action_types:
                    action = action_type.create(session, self.state, **self.kwargs)
                    if action.background:
                        self.running[action] = asyncio.create_task(action.start())
                    else:
                        await self.run_action(action)
                await self.__cancel_background_tasks()
                await asyncio.sleep(1)
            except UserError as error:
                print(type(error))
                print(error.message)
                try:
                    logger.cancel()
                    await logger
                except CancelledError:
                    pass
            except Exception as error:
                traceback.print_exc()

    async def run_action(self, action: Action[Any]) -> None:
        try:
            task = asyncio.create_task(action.start())
            self.running[action] = task
            await task
            self.running.pop(action)
            self.finished.append(action)
        except Exception as error:
            await self.cleanup()
            raise error

    async def __cancel_background_tasks(self) -> None:
        running_items = list(self.running.items())
        for action, task in running_items:
            task.cancel()
            try:
                await task
            except CancelledError:
                pass
            self.running.pop(action)
            self.finished.append(action)

    async def cleanup(self) -> None:
        self.__cancel_running()
        await self.__rollback()

    def __cancel_running(self) -> None:
        running_items = list(self.running.items())
        for action, task in running_items:
            task.cancel()
            self.running.pop(action)
            self.finished.append(action)

    async def __rollback(self) -> None:
        finished = self.finished.copy()
        finished.reverse()
        for action in finished:
            try:
                await action.rollback()
            except Exception:
                pass
