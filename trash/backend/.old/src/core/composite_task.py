from typing import List

from models import Frame, Worker
from models.composite_task import CompositeTask
from schemas.composite_task import CompositeType
from services.tasks import TaskCall


async def distribute_merge_tasks(workers: List[Worker]) -> None:
    frames = await Frame.get_not_merged()
    for worker in workers.copy():
        if len(frames) != 0:
            frame = frames.pop(0)
            await __assign_not_merged(worker, frame)
            workers.remove(worker)
        else:
            break


async def __assign_not_merged(worker: Worker, frame: Frame) -> None:
    composite_task = await CompositeTask.make(frame.id, CompositeType.MERGE)
    frame.merging = True
    await frame.save()
    await composite_task.assign(worker)
    await TaskCall.merge(worker.id, composite_task)
