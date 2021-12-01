from typing import List

from config import Settings
from models import Frame, Subtask, Worker
from services.tasks import TaskCall


async def __calculate_subtask_samples(
    worker: Worker,
    test_worker: Worker,
    remaining_samples: int,
    test_subtask: Subtask,
    settings: Settings,
) -> int:
    if test_subtask.rendered_samples is not None:
        perf_dif = await test_worker.test_time / await worker.test_time
        samples = (
            test_subtask.rendered_samples
            * perf_dif
            * (settings.test_time / settings.task_time)
        )
        if samples > remaining_samples or samples < remaining_samples - 10:
            return remaining_samples
        return int(samples)
    raise Exception("Could not calculate subtask samples")


async def distribute_tested_frames(workers: List[Worker], settings: Settings) -> None:
    frames = await Frame.get_not_distributed()
    for worker in workers.copy():
        if len(frames) != 0:
            frame = frames.pop(0)
            await __assign_tested(worker, frame, settings)
            workers.remove(worker)
            if not frame.distributed:
                frames.insert(0, frame)
        else:
            break


async def distribute_not_tested_frames(
    workers: List[Worker], settings: Settings
) -> None:
    frames = await Frame.get_not_tested()
    for worker in workers.copy():
        if len(frames) != 0:
            frame = frames.pop(0)
            if not frame.tested:
                await __assign_not_tested(worker, frame, settings)
            workers.remove(worker)
        else:
            break


async def __assign_not_tested(worker: Worker, frame: Frame, settings: Settings) -> None:
    task = await frame.task
    subtask = await Subtask.make(frame.id, 0, settings.test_time, task.samples, True)
    await subtask.assign(worker)
    await TaskCall.assign(worker.id, subtask, frame, task)


async def __assign_tested(worker: Worker, frame: Frame, settings: Settings) -> None:
    task = await frame.task
    test_subtask = await frame.test_subtask
    test_worker: Worker = await test_subtask.latest_worker  # type: ignore
    samples_offset = await frame.distributed_samples
    remaining_samples = task.samples - samples_offset
    samples = await __calculate_subtask_samples(
        worker, test_worker, remaining_samples, test_subtask, settings
    )
    subtask = await Subtask.make(
        frame.id, samples_offset, settings.safe_time, samples, False
    )
    await subtask.assign(worker)
    await TaskCall.assign(worker.id, subtask, frame, task)
    if await frame.is_distributed:
        frame.distributed = True
        await frame.save()
