from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas.tasks import TaskCreate, TaskView
from storage import tasks

router = APIRouter(prefix="/tasks")


@router.get("/")
async def get_tasks() -> List[TaskView]:
    return await tasks.get()


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=TaskView)
async def create_task(task: TaskCreate = Depends(TaskCreate.as_form)) -> TaskView:
    return await tasks.create(task)


@router.get("/{task_id}", response_model=TaskView)
async def get_task_by_id(task_id: UUID) -> Optional[TaskView]:
    return await tasks.get_by_id(task_id)
