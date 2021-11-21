from uuid import UUID

from fastapi_websocket_rpc import RpcMethodsBase

from core import channel as ChannelCore
from schemas.subtasks import SubtaskView


class TasksService(RpcMethodsBase):
    async def task_status(self) -> None:
        print(self.channel)


class TaskCall:
    async def assign(self, worker_id: UUID, subtask: SubtaskView) -> None:
        channel = ChannelCore.get(worker_id)
