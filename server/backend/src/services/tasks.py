from uuid import UUID

from fastapi_websocket_rpc import RpcMethodsBase

from core import channel as ChannelCore
from models import CompositeTask, Frame, Subtask, Task
from schemas.composite_task import MergeTaskData
from schemas.subtask import SubtaskData


class TasksService(RpcMethodsBase):
    async def task_status(self) -> None:
        print(self.channel)


class TaskCall:
    @staticmethod
    def __create_send_task(subtask: Subtask, frame: Frame, task: Task) -> SubtaskData:
        return SubtaskData(
            task_id=task.id,
            subtask_id=subtask.id,
            frame_nr=frame.nr,
            samples_offset=subtask.samples_offset,
            time_limit=subtask.time_limit,
            max_samples=subtask.max_samples,
            resolution_x=task.resolution_x,
            resolution_y=task.resolution_y,
        )

    @staticmethod
    async def __create_merge_task(composite_task: CompositeTask) -> MergeTaskData:

        return MergeTaskData(
            composite_task_id=composite_task.id,
            subtask_data=await composite_task.merge_data,
        )

    @staticmethod
    async def assign(
        worker_id: UUID, subtask: Subtask, frame: Frame, task: Task
    ) -> None:
        send_task = TaskCall.__create_send_task(subtask, frame, task)
        channel = ChannelCore.get(worker_id)
        await channel.other.new_task(task=send_task)

    @staticmethod
    async def merge(worker_id: UUID, composite_task: CompositeTask) -> None:
        merge_task = await TaskCall.__create_merge_task(composite_task)
        channel = ChannelCore.get(worker_id)
        await channel.other.merge_task(task=merge_task)
