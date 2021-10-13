import os
from typing import List
from uuid import UUID

import aiofiles
from fastapi import UploadFile
from tortoise.transactions import atomic

from config import Settings
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskView


@atomic()
async def create(task: TaskCreate, settings: Settings) -> TaskView:
    task_model = Task(**task.dict(), name=task.file.filename)
    await task_model.save()
    await __write_file_to_disk(task.file, task_model.id, settings.task_dir)
    return TaskView.from_orm(task_model)


async def __write_file_to_disk(file: UploadFile, uuid: UUID, task_dir: str) -> None:
    path = os.path.join(task_dir, uuid.hex + ".blend")
    async with aiofiles.open(path, "wb+") as out_file:
        while content := await file.read(1024):
            if isinstance(content, bytes):
                await out_file.write(content)


async def get() -> List[TaskView]:
    tasks = await Task.all()
    task_views: List[TaskView] = []
    for task in tasks:
        task_views.append(TaskView.from_orm(task))
    return task_views


async def get_by_id(task_id: UUID) -> TaskView:
    task_db = await Task.get(id=task_id)
    return TaskView.from_orm(task_db)


async def delete(task_id: UUID) -> None:
    task_db = await Task.get(id=task_id)
    await task_db.delete()
