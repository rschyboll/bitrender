from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, File, Form
from fastapi.datastructures import UploadFile

from tortoise.transactions import atomic

from models import CompositeTask
from core import task as TaskCore

router = APIRouter(prefix="/composite_task")


@router.post("/success")
@atomic()
async def success(
    background_tasks: BackgroundTasks,
    composite_task_id: UUID = Form(...),
    file: UploadFile = File(...),
) -> None:
    composite_task = await CompositeTask.get_by_id(composite_task_id)
    await composite_task.set_finished(file)
    frame = await composite_task.frame
    task = await frame.task
    await frame.update()
    await task.update()
    background_tasks.add_task(TaskCore.distribute_tasks)


@router.post("/error")
@atomic()
async def error(
    background_tasks: BackgroundTasks,
    composite_task_id: UUID = Form(...),
) -> None:
    composite_task = await CompositeTask.get_by_id(composite_task_id)
    await composite_task.set_failed()    
    frame = await composite_task.frame
    task = await frame.task
    await frame.update()
    await task.update()
    background_tasks.add_task(TaskCore.distribute_tasks)
