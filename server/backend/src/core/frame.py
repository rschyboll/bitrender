from typing import List

from tortoise.transactions import atomic

from config import Settings
from models import Frame, Subtask, SubtaskAssign, Task, Worker
from schemas import SubtaskAssignCreate, SubtaskCreate
from services.tasks import TaskCall


async def __create_assign(subtask: Subtask, worker: Worker) -> SubtaskAssign:
    subtask_create = SubtaskAssignCreate(subtask_id=subtask.id, worker_id=worker.id)
    return await SubtaskAssign.from_create(subtask_create)


async def __calculate_samples(
    frame: Frame,
    worker: Worker,
    test_worker: Worker,
    test_subtask: Subtask,
    task: Task,
    settings: Settings,
) -> int:
    if (
        worker.test is not None
        and test_worker.test is not None
        and test_subtask.rendered_samples is not None
    ):
        worker_test = await worker.test
        test_worker_test = await test_worker.test
        if worker_test is not None and test_worker_test is not None:
            max_samples = task.samples - (await frame.get_samples_sum())
            performance_dif = (
                test_worker_test.render_time - test_worker_test.sync_time
            ) / (worker_test.render_time - worker_test.sync_time)
            samples = (
                test_subtask.rendered_samples
                * performance_dif
                * (settings.test_time / settings.task_time)
            )
            samples = min(samples, max_samples)
            return int(samples)
    return task.samples


async def distribute_frames(workers: List[Worker], settings: Settings) -> None:
    frames = await Frame.get_not_running()
    for worker in workers.copy():
        if len(frames) != 0:
            frame = frames.pop(0)
            await assign_frame_to_worker(worker, frame, settings)
            workers.remove(worker)
        else:
            break


async def assign_frame_to_worker(
    worker: Worker, frame: Frame, settings: Settings
) -> None:
    task = await frame.task
    if not frame.tested:
        subtask_create = SubtaskCreate(
            frame_id=frame.id,
            seed=0,
            time_limit=settings.test_time,
            max_samples=task.samples,
            test=True,
        )
    else:
        test_subtask = await frame.get_test_subtask()
        last_subtask = await frame.get_latest_subtask()
        if test_subtask is not None and last_subtask is not None:
            test_subtask_assign = await test_subtask.get_latest_assign()
            if test_subtask_assign is not None:
                test_subtask_worker = await test_subtask_assign.worker
                subtask_create = SubtaskCreate(
                    frame_id=frame.id,
                    seed=last_subtask.seed + 1,
                    time_limit=settings.safe_time,
                    max_samples=__calculate_samples(
                        frame, worker, test_subtask_worker, test_subtask, task, settings
                    ),
                    test=False,
                )
    subtask = await Subtask.from_create(subtask_create)
    await __create_assign(subtask, worker)
    await TaskCall.assign(worker.id, subtask, frame, task)
