from typing import List, Optional, Tuple

from tortoise.transactions import atomic, in_transaction

from models import Frame, Subtask, SubtaskAssign, Task, Worker
from schemas import SubtaskAssignCreate
from services.tasks import TaskCall


async def __create_assign(subtask: Subtask, worker: Worker) -> SubtaskAssign:
    subtask_create = SubtaskAssignCreate(subtask_id=subtask.id, worker_id=worker.id)
    return await SubtaskAssign.from_create(subtask_create)


async def __get_subtask_data(
    subtask: Subtask,
) -> Tuple[Frame, Task, Optional[SubtaskAssign]]:
    frame = await subtask.frame
    task = await frame.task
    assign = await subtask.latest_assign
    return frame, task, assign


async def distribute_subtasks(workers: List[Worker]) -> None:
    subtasks = await Subtask.get_not_assigned()
    for worker in workers.copy():
        if len(subtasks) != 0:
            subtask = subtasks.pop(0)
            await assign_subtask(worker, subtask)
            workers.remove(worker)
        else:
            break


async def assign_subtask(worker: Worker, subtask: Subtask) -> None:
    async with in_transaction():
        frame, task, last_assign = await __get_subtask_data(subtask)
        if not subtask.test and last_assign is not None:
            await update_subtask(subtask, worker, last_assign, task, frame)
        await __create_assign(subtask, worker)
        subtask.assigned = True
        await subtask.save()
        await TaskCall.assign(worker.id, subtask, frame, task)


async def update_subtask(
    subtask: Subtask,
    worker: Worker,
    last_assign: SubtaskAssign,
    task: Task,
    frame: Frame,
) -> None:
    await update_subtask_samples(worker, subtask, last_assign, task, frame)
    if await frame.assigned_samples_sum != task.samples:
        frame.assigned = False
    else:
        frame.assigned = True
    await frame.save()


async def update_subtask_samples(
    worker: Worker, subtask: Subtask, assign: SubtaskAssign, task: Task, frame: Frame
) -> None:
    test_worker = await assign.worker
    test_worker_test = await test_worker.get_test()
    worker_test = await worker.get_test()
    if test_worker_test is not None and worker_test is not None:
        max_samples = task.samples - (await frame.assigned_samples_sum)
        performance_dif = (
            test_worker_test.render_time - test_worker_test.sync_time
        ) / (worker_test.render_time - worker_test.sync_time)
        new_samples = subtask.max_samples * performance_dif
        new_samples = min(new_samples, max_samples)
        subtask.max_samples = int(new_samples)
        await subtask.save()
