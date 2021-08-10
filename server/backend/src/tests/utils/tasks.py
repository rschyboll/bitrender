import io
import random
from uuid import UUID
from typing import List, Tuple

from fastapi import UploadFile

from models.tasks import Task
from schemas.tasks import TaskCreate, Engines
from tests.utils import random_lower_string


def random_task_data() -> TaskCreate:
    name = random_lower_string()
    engine = random.choice(list(Engines))
    samples = random.randint(0, 10000)
    file = io.BytesIO(random_lower_string(random.randint(100, 10000)).encode())
    upload_file = UploadFile(name, file)
    return TaskCreate(file=upload_file, engine=engine, samples=samples)


async def init_random_task_data() -> List[Tuple[UUID, TaskCreate]]:
    data: List[Tuple[UUID, TaskCreate]] = []
    for _ in range(0, random.randint(10, 100)):
        task_in = random_task_data()
        task = Task(**task_in.dict(), name=task_in.file.filename)
        await task.save()
        data.append((task.id, task_in))
    return data
