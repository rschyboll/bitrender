import os
from typing import List, Optional
from uuid import UUID

from config import Settings, get_settings
from core import task as TasksCore
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import FileResponse
from models import Task
from schemas import TaskCreate, TaskView

router = APIRouter(prefix="/tasks")


@router.get("/")
async def get_tasks() -> List[TaskView]:
    return await Task.get_all(True)


@router.get("/test_task")
async def get_test_task() -> FileResponse:
    return FileResponse("../resources/test.blend")


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_task(
    background_tasks: BackgroundTasks,
    task_create: TaskCreate = Depends(TaskCreate.as_form),
    settings: Settings = Depends(get_settings),
) -> TaskView:
    task = await Task.make(**task_create.dict())
    background_tasks.add_task(TasksCore.new_task, task, settings)
    return task.to_view()


@router.get("/result/{task_id}")
async def get_task_result(task_id: UUID) -> FileResponse:
    task = await Task.get_by_id(task_id)
    if os.path.exists(task.zip_path):
        return FileResponse(task.zip_path)
    raise HTTPException(404)


@router.get("/{task_id}")
async def get_task_by_id(task_id: UUID) -> Optional[TaskView]:
    return await Task.get_by_id(task_id, True)


@router.delete("/{task_id}")
async def delete_task(task_id: UUID) -> None:
    await (await Task.get_by_id(task_id)).delete()


@router.get("/file/{task_id}")
async def get_task_file(task_id: UUID, settings: Settings = Depends(get_settings)) -> FileResponse:
    path = os.path.join(settings.task_dir, task_id.hex)
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(404)
