import os
from typing import List, Optional
from uuid import UUID

import aiofiles
from fastapi import UploadFile
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from config import get_settings
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskView

settings = get_settings()


@atomic()
async def create(task: TaskCreate) -> TaskView:
    task_model = Task(**task.dict(), name=task.file.filename)
    await task_model.save()
    await __write_file_to_disk(task.file, task_model.id)
    return TaskView.from_orm(task_model)


async def __write_file_to_disk(file: UploadFile, uuid: UUID) -> None:
    path = os.path.join(settings.task_files_path, uuid.hex + ".blend")
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


async def get_by_id(task_id: UUID) -> Optional[TaskView]:
    try:
        task_db = await Task.get(id=task_id)
        return TaskView.from_orm(task_db)
    except DoesNotExist:
        return None


async def delete(task_id: UUID) -> None:
    try:
        task_db = await Task.get(id=task_id)
        await task_db.delete()
    except DoesNotExist:
        return
