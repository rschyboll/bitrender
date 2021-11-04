import asyncio
import os
from asyncio import Task
from typing import Any, Dict, List

from app.action import Action


def clear_console() -> None:
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


class Logger:
    def __init__(
        self, running: Dict[Action[Any], Task[None]], finished: List[Action[Any]]
    ):
        self.running = running
        self.finished = finished

    async def start(self) -> None:
        while False:
            clear_console()
            for action in self.finished:
                self.print_action(action, True)
            for action in self.running.keys():
                self.print_action(action, False)
            await asyncio.sleep(0.1)

    def print_action(
        self, action: Action[Any], finished: bool, offset: str = ""
    ) -> None:
        if finished:
            print(offset + "✔   " + type(action).__name__)
        elif action.background:
            print(offset + "🗘   " + type(action).__name__)
        else:
            print(offset + "✘   " + type(action).__name__)
        for sub_action in action.finished:
            self.print_action(sub_action, True, offset + "  ")
        for sub_action in action.running:
            self.print_action(sub_action, False, offset + "  ")
