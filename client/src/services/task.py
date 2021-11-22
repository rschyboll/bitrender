from typing import TYPE_CHECKING, Any

from actions.task import Task
from app.action import Action
from core.task import TaskData

if TYPE_CHECKING:
    from services import RPCClient
else:
    RPCClient = object


class TaskClient:
    def __init__(self, action: Action[Any]):
        self.action = action

    async def new_task(self, task: dict[str, Any]) -> None:
        task_data = TaskData(**task)
        await self.action.start_background_subaction(Task, task_data=task_data)


class TaskCall:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client
