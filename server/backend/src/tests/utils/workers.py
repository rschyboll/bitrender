import io
import random
from typing import List, Tuple
from uuid import UUID

from models.workers import Worker
from schemas.workers import WorkerCreate
from tests.utils import random_lower_string


def random_task_data() -> WorkerCreate:
    name = random_lower_string()
    samples = random.randint(0, 10000)
    return WorkerCreate(file=upload_file, engine=engine, samples=samples)


async def init_random_task_data() -> List[Tuple[UUID, TaskCreate]]:
    data: List[Tuple[UUID, TaskCreate]] = []
    for _ in range(0, random.randint(10, 100)):
        task_in = random_task_data()
        task = Task(**task_in.dict(), name=task_in.file.filename)
        await task.save()
        data.append((task.id, task_in))
    return data
