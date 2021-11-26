from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form
from fastapi.datastructures import UploadFile

from config import Settings, get_settings
from core import task as TasksCore
from models import Subtask

router = APIRouter(prefix="/subtasks")


@router.post("/success")
async def success(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> None:
    pass


@router.post("/error")
async def error(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> None:
    pass
