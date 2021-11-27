from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form
from fastapi.datastructures import UploadFile

from config import Settings, get_settings
from core import task as TaskCore
from models import Subtask

router = APIRouter(prefix="/subtasks")


@router.post("/success")
async def success(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    samples: int = Form(...),
    file: UploadFile = File(...),
) -> None:
    subtask = await Subtask.get_by_id(subtask_id)
    await subtask.set_finished(samples, file)
    await TaskCore.update_subtasks_status(subtask)
    background_tasks.add_task(TaskCore.distribute_tasks)


@router.post("/error")
async def error(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
) -> None:
    subtask = await Subtask.get_by_id(subtask_id)
    subtask.error = True
    await subtask.save()
    background_tasks.add_task(TaskCore.distribute_tasks)
