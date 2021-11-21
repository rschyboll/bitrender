from tortoise.transactions import atomic

from config import Settings
from core import worker as WorkerCore
from schemas.frames import FrameCreate, FrameView
from schemas.subtasks import SubtaskCreate, SubtaskView
from schemas.tasks import TaskView
from schemas.workers import WorkerUpdate, WorkerView
from storage import tasks as TaskStorage
from storage import frames as FrameStorage
from storage import subtasks as SubtaskStorage
from storage import workers as WorkerStorage
from storage import subtask_assignments as SubtaskAssignmentStorage


async def new_task(task: TaskView, settings: Settings) -> None:
    for frame_nr in range(task.start_frame, task.end_frame + 1):
        frame = FrameCreate(nr=frame_nr, task_id=task.id)
        await FrameStorage.create(frame)
    await distribute_tasks(settings)


@atomic()
async def distribute_tasks(settings: Settings) -> None:
    test = await WorkerStorage.get_idle()
    workers = await WorkerCore.filter_connected(await WorkerStorage.get_idle())
    subtasks = await SubtaskStorage.get_not_assigned()
    if len(subtasks) != 0 and len(workers) != 0:
        for worker in workers.copy():
            if len(subtasks) != 0:
                subtask = subtasks.pop(0)
                await assign_subtask_to_worker(worker, subtask, settings)
                workers.remove(worker)
            else:
                break
    frames = await FrameStorage.get_not_running()
    if len(frames) != 0 and len(workers) != 0:
        for worker in workers.copy():
            if len(frames) != 0:
                frame = frames.pop(0)
                task = await TaskStorage.get_by_frame_id(frame.id)
                await assign_frame_to_worker(worker, frame, task, settings)
                workers.remove(worker)
            else:
                break


@atomic()
async def assign_subtask_to_worker(
    worker: WorkerView,
    subtask: SubtaskView,
    task: TaskView,
    settings: Settings,
) -> None:
    worker_update = WorkerUpdate(id=worker.id, subtask_id=subtask.id)


@atomic()
async def assign_frame_to_worker(
    worker: WorkerView,
    frame: FrameView,
    task: TaskView,
    settings: Settings,
) -> None:
    if not frame.tested:
        subtask = SubtaskCreate(frame_id=frame.id, seed=0)
    else:
        pass
