from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse

from schemas.tasks import TaskCreate, TaskView
from storage import tasks

router = APIRouter(prefix="/tasks")


@router.get("/")
async def get_tasks() -> List[TaskView]:
    return await tasks.get()


@router.get("/test_app")
async def get_test_app() -> FileResponse:
    return FileResponse("../resources/classroom.blend")


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate = Depends(TaskCreate.as_form)) -> TaskView:
    return await tasks.create(task)


@router.get("/{task_id}")
async def get_task_by_id(task_id: UUID) -> Optional[TaskView]:
    return await tasks.get_by_id(task_id)
