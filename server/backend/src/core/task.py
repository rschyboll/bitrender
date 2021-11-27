from tortoise.transactions import atomic

from config import Settings, get_settings
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
async def update_subtasks_status(
    subtask: Subtask, settings: Settings = get_settings()
) -> None:
    frame = await subtask.frame
    task = await frame.task
    if await frame.rendered_samples_sum == task.samples:
        if await frame.subtasks_count == 1:
            frame.merged = True
            await subtask.copy_subtask_to_frame()
        frame.finished = True
    if subtask.test:
        frame.tested = True
    if await task.finished_frames_count == task.end_frame - task.start_frame:
        task.finished = True
    await frame.save()
    await task.save()

@atomic()
async def distribute_tasks(settings: Settings = get_settings()) -> None:
    workers = await WorkerCore.filter_connected(await Worker.get_idle())
    await SubtaskCore.distribute_subtasks(workers)
    await FrameCore.distribute_tested_frames(workers, settings)
    await FrameCore.distribute_not_tested_frames(workers, settings)
    print("TEST")
