import os
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.responses import FileResponse

from tortoise.transactions import atomic

from core import task as TaskCore
from models import Subtask

router = APIRouter(prefix="/subtasks")


@router.post("/success")
@atomic()
async def success(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
    samples: int = Form(...),
    file: UploadFile = File(...),
) -> None:
    subtask = await Subtask.get_by_id(subtask_id)
    frame = await subtask.frame
    task = await frame.task
    if subtask.test:
        frame.testing = False
    await subtask.set_finished(samples, file)
    await frame.update()
    await task.update()
    background_tasks.add_task(TaskCore.distribute_tasks)


@router.post("/error")
@atomic()
async def error(
    background_tasks: BackgroundTasks,
    subtask_id: UUID = Form(...),
) -> None:
    subtask = await Subtask.get_by_id(subtask_id)
    frame = await subtask.frame
    task = await frame.task
    if subtask.test:
        frame.testing = False
    await subtask.set_failed()
    await frame.update()
    await task.update()
    background_tasks.add_task(TaskCore.distribute_tasks)


@router.get("/file/{subtask_id}")
async def get_subtask_file(subtask_id: UUID) -> FileResponse:
    subtask = await Subtask.get_by_id(subtask_id)
    if os.path.exists(subtask.path):
        return FileResponse(subtask.path)
    raise HTTPException(404)
