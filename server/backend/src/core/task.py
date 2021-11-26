from tortoise.transactions import atomic

from config import Settings
from core import frame as FrameCore
from core import subtask as SubtaskCore
from core import worker as WorkerCore
from models import Frame, Subtask, Task, Worker
from schemas import FrameCreate, SubtaskCreate
from services.tasks import TaskCall


async def new_task(task: Task, settings: Settings) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        frame_create = FrameCreate(nr=frame_nr, task_id=task.id)
        await Frame.from_create(frame_create)
    await distribute_tasks(settings)


@atomic()
async def distribute_tasks(settings: Settings) -> None:
    workers = await WorkerCore.filter_connected(await Worker.get_idle())
    await SubtaskCore.distribute_subtasks(workers)
    await FrameCore.distribute_frames(workers, settings)
