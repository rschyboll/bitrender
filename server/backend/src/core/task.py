from core import worker as WorkerCore
from schemas.frames import FrameCreate
from schemas.tasks import TaskView
from schemas.subtasks import SubtaskCreate
from storage import frames as FrameStorage
from storage import workers as WorkerStorage
from storage import subtasks as SubtaskStorage


async def new_task(task: TaskView) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        frame = FrameCreate(nr=frame_nr, task_id=task.id)
        await FrameStorage.create(frame)
    await distribute_tasks()


async def distribute_tasks() -> None:
    workers = await WorkerCore.filter_connected(await WorkerStorage.get_idle())
    frames = await FrameStorage.get_not_finished()
    if len(frames) != 0:
        not_running_frames = await FrameStorage.get_not_running()


async def get_last_not_finished_task() -> None:
    pass
