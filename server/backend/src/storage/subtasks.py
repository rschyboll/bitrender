import os
from typing import List
from uuid import UUID

import aiofiles
from fastapi import UploadFile
from tortoise.transactions import atomic

from config import Settings
from models.subtasks import Subtask
from schemas.subtasks import SubtaskCreate, SubtaskView


async def create(subtask: SubtaskCreate) -> SubtaskView:
    subtask_db = Subtask(**subtask.dict())
    await subtask_db.save()
    return SubtaskView.from_orm(subtask_db)


async def get() -> List[SubtaskView]:
    subtasks = await Subtask.all()
    subtask_views: List[SubtaskView] = []
    for subtask in subtasks:
        subtask_views.append(SubtaskView.from_orm(subtask))
    return subtask_views


@atomic()
async def set_finished(subtask_id: UUID, file: UploadFile, settings: Settings) -> None:
    subtask = Subtask.filter(id=subtask_id)
    await __write_file_to_disk(file, subtask_id, settings.subtask_dir)
    await subtask.update(finished=True)


async def __write_file_to_disk(file: UploadFile, uuid: UUID, subtask_dir: str) -> None:
    path = os.path.join(subtask_dir, uuid.hex + ".exr")
    async with aiofiles.open(path, "wb+") as out_file:
        while content := await file.read(1024):
            if isinstance(content, bytes):
                await out_file.write(content)


async def get_running_frames() -> None:
    pass
