from typing import Any, TYPE_CHECKING

from actions.task import Task
from app.action import Action

if TYPE_CHECKING:
    from services import RPCClient
else:
    RPCClient = object


class TaskClient:
    def __init__(self, action: Action[Any]):
        super().__init__()
        self.action = action

    async def new_task(self) -> None:
        await self.action.start_background_subaction(Task)


class TaskCall:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client
