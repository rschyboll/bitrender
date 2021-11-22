from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form
from fastapi.datastructures import UploadFile

from config import Settings, get_settings
from core import task as TasksCore
from storage import subtasks as SubtasksStorage

router = APIRouter(prefix="/subtasks")


@router.post("/success")
async def success(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> None:
    await SubtasksStorage.set_finished(subtask_id, file, settings)
    background_tasks.add_task(TasksCore.distribute_tasks, settings)


@router.post("/error")
async def error(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> None:
    pass
