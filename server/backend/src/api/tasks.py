from fastapi import APIRouter, Depends, status

from schemas.tasks import TaskIn
from storage import tasks

router = APIRouter(prefix="/tasks")


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskIn = Depends(TaskIn.as_form)) -> None:
    await tasks.create(task)
