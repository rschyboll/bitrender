from __future__ import annotations
from typing import List, Any

from abc import ABC, abstractmethod


class Action(ABC):
    sub_actions: List[Action]
    required: bool
    critical: bool

    def __init__(self):
        pass

    @abstractmethod
    async def start(self) -> Any:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
