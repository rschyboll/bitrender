from typing import List

from models import Frame, Subtask, Task, Worker
from services.tasks import TaskCall
from config import get_settings


async def distribute_subtasks(workers: List[Worker]) -> None:
    subtasks = await Subtask.get_not_assigned()
    for worker in workers.copy():
        if len(subtasks) != 0:
            subtask = subtasks.pop(0)
            await assign_subtask(worker, subtask)
            workers.remove(worker)
        else:
            break


async def assign_subtask(worker: Worker, subtask: Subtask) -> List[Subtask]:
    new_subtasks: List[Subtask] = []
    frame = await subtask.frame
    task = await frame.task
    if subtask.test:
        pass
    else:
        test_subtask = await frame.test_subtask
        test_worker = await test_subtask.latest_worker
        if test_worker is not None:
            new_subtasks.extend(
                await update_subtask(subtask, worker, test_worker, task, frame)
            )
    await subtask.assign(worker)
    await TaskCall.assign(worker.id, subtask, frame, task)
    return new_subtasks


async def update_subtask(
    subtask: Subtask, worker: Worker, test_worker: Worker, task: Task, frame: Frame
) -> List[Subtask]:
    settings = get_settings()
    new_subtasks: List[Subtask] = []
    new_samples = await get_new_samples(worker, subtask, test_worker)
    if new_samples < subtask.max_samples:
        new_subtask = await Subtask.make(
            frame.id,
            subtask.samples_offset + new_samples,
            settings.task_time,
            subtask.max_samples - subtask.samples_offset + new_samples,
            False,
        )
        new_subtasks.append(new_subtask)
    subtask.max_samples = new_samples
    await subtask.save()
    return new_subtasks


async def get_new_samples(worker: Worker, subtask: Subtask, test_worker: Worker) -> int:
    perf_dif = await test_worker.test_time / await worker.test_time
    new_samples = subtask.max_samples * perf_dif
    if new_samples < subtask.max_samples:
        pass
    elif new_samples >= subtask.max_samples:
        new_samples = subtask.max_samples
    return int(new_samples)
