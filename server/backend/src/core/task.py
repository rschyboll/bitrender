from schemas.tasks import TaskView
from schemas.frames import FrameCreate
from storage import frames as FrameStorage
from storage import workers as WorkerStorage
from core import worker as WorkerCore


async def new_task(task: TaskView) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        frame = FrameCreate(nr=frame_nr, task_id=task.id)
        await FrameStorage.create(frame)
    await distribute_tasks()


async def distribute_tasks() -> None:
    workers = await WorkerStorage.get_idle()
    workers = await WorkerCore.filter_connected(workers)
    print(workers)


async def get_last_not_finished_task() -> None:
    pass
