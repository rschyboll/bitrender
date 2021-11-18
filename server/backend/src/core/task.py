from core import worker as WorkerCore
from schemas.frames import FrameCreate
from schemas.subtasks import SubtaskCreate
from schemas.tasks import TaskView
from storage import frames as FrameStorage
from storage import subtasks as SubtaskStorage
from storage import workers as WorkerStorage
from tortoise.transactions import atomic


async def new_task(task: TaskView) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        frame = FrameCreate(nr=frame_nr, task_id=task.id)
        await FrameStorage.create(frame)
    await distribute_tasks()


@atomic()
async def distribute_tasks() -> None:
    workers = await WorkerCore.filter_connected(await WorkerStorage.get_idle())
    subtasks = await SubtaskStorage.get_not_assigned()
    frames = await FrameStorage.get_not_running()
    if (len(frames) != 0 or len(subtasks) != 0) and len(workers) != 0:
        for worker in workers:
            if len(subtasks) != 0:
                subtask = subtasks.pop(0)
                print(subtask)


async def assign_subtask_to_worker() -> None:
    pass
