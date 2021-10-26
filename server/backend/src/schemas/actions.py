from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID


class ActionType(str, Enum):
    TEST = "TEST"
    RUN = "RUN"


class Action:
    def __init__(
        self,
        type: ActionType,
        task: Optional[UUID] = None,
        subtask: Optional[UUID] = None,
    ):
        self.type = type
        self.task = task
        self.subtask = subtask

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "task": self.task, "subtask": self.subtask}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Action:
        if "type" in data and "task" in data and "subtask" in data:
            action_type = ActionType[data["type"]]
            task = UUID(hex=data["task"])
            subtask = UUID(hex=data["subtask"])
            return Action(action_type, task, subtask)
        raise ValueError()
