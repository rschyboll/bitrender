import os
import aiofiles
from typing import List
from fastapi import UploadFile
from tortoise.transactions import atomic
from pydantic.types import UUID4

from config import get_settings
from schemas.tasks import TaskIn, TaskView
from models.tasks import Task

settings = get_settings()


@atomic()
async def create(task: TaskIn) -> TaskView:
    task_model = Task(**task.dict(), name=task.file.filename)
    await task_model.save()
    await write_file_to_disk(task.file, task_model.id)
    return TaskView.from_orm(task_model)


async def write_file_to_disk(file: UploadFile, uuid: UUID4) -> None:
    path = os.path.join("..", settings.task_files_path, uuid.hex + ".blend")
    async with aiofiles.open(path, "wb+") as out_file:
        while content := await file.read(1024):
            if isinstance(content, bytes):
                await out_file.write(content)
            elif isinstance(content, str):
                await out_file.write(content.encode())


async def get() -> List[TaskView]:
    tasks = await Task.all()
    task_views: List[TaskView] = []
    for task in tasks:
        task_views.append(TaskView.from_orm(task))

    return task_views


async def get_by_id(id: str):
    uuid = UUID4(id)
