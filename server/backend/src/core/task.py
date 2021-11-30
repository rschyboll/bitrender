from tortoise.transactions import atomic

from config import Settings, get_settings
from core import frame as FrameCore
from core import subtask as SubtaskCore
from core import worker as WorkerCore
from models import Frame, Task, Worker
from schemas import FrameCreate


async def new_task(task: Task, settings: Settings) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        await Frame.make(task.id, frame_nr)
    await distribute_tasks(settings)


@atomic()
async def distribute_tasks(settings: Settings = get_settings()) -> None:
    workers = await WorkerCore.filter_connected(await Worker.get_idle())
    await SubtaskCore.distribute_subtasks(workers)
    await FrameCore.distribute_tested_frames(workers, settings)
    await FrameCore.distribute_not_tested_frames(workers, settings)
