from __future__ import annotations
from typing import Optional, Dict, Any
from uuid import UUID
from enum import Enum
import json


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
            action_type = ActionType(data["type"])
            if data["task"] is not None:
                task = UUID(hex=data["task"])
            else:
                task = None
            if data["subtask"] is not None:
                subtask = UUID(hex=data["subtask"])
            else:
                subtask = None
            return Action(action_type, task, subtask)
        raise ValueError()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data: str) -> Action:
        return Action.from_dict(json.loads(data))
