import os
from typing import List
from uuid import UUID

from fastapi import UploadFile

from config import Settings
from models.subtask import Subtask
from schemas.subtask import SubtaskCreate, SubtaskView
from utils import save_file


async def create(subtask: SubtaskCreate) -> Subtask:
    subtask_db = Subtask(**subtask.dict())
    await subtask_db.save()
    return subtask_db


async def get() -> List[Subtask]:
    return await Subtask.all().select_for_update()


async def get_view() -> List[SubtaskView]:
    subtasks = await Subtask.all()
    return __to_view_list(subtasks)


async def get_by_id(subtask_id: UUID) -> Subtask:
    return await Subtask.all().select_for_update().get(id=subtask_id)


async def get_view_by_id(subtask_id: UUID) -> SubtaskView:
    return (await Subtask.get(id=subtask_id)).to_view()


async def get_not_assigned() -> List[Subtask]:
    return await Subtask.filter(assigned=False, finished=False).select_for_update()


async def save_result(subtask_id: UUID, file: UploadFile, settings: Settings) -> None:
    path = os.path.join(settings.subtask_dir, subtask_id.hex + ".exr")
    await save_file(path, file)


def __to_view_list(subtasks: List[Subtask]) -> List[SubtaskView]:
    views: List[SubtaskView] = []
    for subtask in subtasks:
        views.append(subtask.to_view())
    return views
