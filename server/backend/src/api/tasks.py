from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import FileResponse

from core import task as TasksCore
from schemas.tasks import TaskCreate, TaskView
from storage import tasks
from config import Settings, get_settings

router = APIRouter(prefix="/tasks")


@router.get("/")
async def get_tasks() -> List[TaskView]:
    return await tasks.get()


@router.get("/test_task")
async def get_test_task() -> FileResponse:
    return FileResponse("../resources/test.blend")


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_task(
    background_tasks: BackgroundTasks,
    task: TaskCreate = Depends(TaskCreate.as_form),
    settings: Settings = Depends(get_settings),
) -> TaskView:
    task_view = await tasks.create(task, settings)
    background_tasks.add_task(TasksCore.new_task, task_view)
    return task_view


@router.get("/{task_id}")
async def get_task_by_id(task_id: UUID) -> Optional[TaskView]:
    return await tasks.get_by_id(task_id)


@router.delete("/{task_id}")
async def delete_task(task_id: UUID) -> None:
    await tasks.delete(task_id)
