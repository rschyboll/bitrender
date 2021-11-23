from uuid import UUID

from fastapi_websocket_rpc import RpcMethodsBase
from pydantic import BaseModel

from core import channel as ChannelCore
from schemas.frames import FrameView
from schemas.subtask import SubtaskView
from schemas.tasks import TaskView


class TaskData(BaseModel):
    task_id: UUID
    subtask_id: UUID
    frame_nr: int
    seed: int
    time_limit: int
    max_samples: int
    resolution_x: int
    resolution_y: int


class TasksService(RpcMethodsBase):
    async def task_status(self) -> None:
        print(self.channel)


class TaskCall:
    @staticmethod
    def __create_send_task(
        subtask: SubtaskView, frame: FrameView, task: TaskView
    ) -> TaskData:
        return TaskData(
            task_id=task.id,
            subtask_id=subtask.id,
            frame_nr=frame.nr,
            seed=subtask.seed,
            time_limit=subtask.time_limit,
            max_samples=subtask.max_samples,
            resolution_x=task.resolution_x,
            resolution_y=task.resolution_y,
        )

    @staticmethod
    async def assign(
        worker_id: UUID, subtask: SubtaskView, frame: FrameView, task: TaskView
    ) -> None:
        send_task = TaskCall.__create_send_task(subtask, frame, task)
        channel = ChannelCore.get(worker_id)
        await channel.other.new_task(task=send_task)
