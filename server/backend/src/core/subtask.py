from typing import List

from tortoise.transactions import atomic

from models import Frame, Subtask, SubtaskAssign, Task, Worker
from schemas import SubtaskAssignCreate
from services.tasks import TaskCall


async def __create_assign(subtask: Subtask, worker: Worker) -> SubtaskAssign:
    subtask_create = SubtaskAssignCreate(subtask_id=subtask.id, worker_id=worker.id)
    return await SubtaskAssign.from_create(subtask_create)


@atomic()
async def distribute_subtasks(workers: List[Worker]) -> None:
    subtasks = await Subtask.get_not_assigned()
    for worker in workers.copy():
        if len(subtasks) != 0:
            subtask = subtasks.pop(0)
            await assign_subtask(worker, subtask)
            subtasks.remove(subtask)
        else:
            break


@atomic()
async def assign_subtask(worker: Worker, subtask: Subtask) -> None:
    frame = await subtask.frame
    task = await frame.task
    if not subtask.test:
        old_assign = await subtask.get_latest_assign()
        if old_assign is not None:
            await update_subtask_samples(worker, subtask, old_assign, task, frame)
    await __create_assign(subtask, worker)
    await TaskCall.assign(worker.id, subtask, frame, task)


async def update_subtask_samples(
    worker: Worker, subtask: Subtask, assign: SubtaskAssign, task: Task, frame: Frame
) -> None:
    old_worker = await assign.worker
    if old_worker.test is not None and worker.test is not None:
        old_worker_test = await old_worker.test
        worker_test = await worker.test
        if old_worker_test is not None and worker_test is not None:
            max_samples = task.samples - (await frame.get_samples_sum())
            performance_dif = (
                old_worker_test.render_time - old_worker_test.sync_time
            ) / (worker_test.render_time - worker_test.sync_time)
            new_samples = subtask.max_samples * performance_dif
            new_samples = min(new_samples, max_samples)
            subtask.max_samples = int(new_samples)
            await subtask.save()
