import os
from typing import List
from uuid import UUID

from fastapi import UploadFile

from config import Settings
from models.frames import Frame
from schemas.frames import FrameCreate, FrameView
from utils import save_file


async def get() -> List[Frame]:
    return await Frame.all().select_for_update()


async def get_view() -> List[FrameView]:
    frames = await Frame.all()
    return __to_view_list(frames)


async def get_by_id(frame_id: UUID) -> Frame:
    return await Frame.all().select_for_update().get(id=frame_id)


async def get_view_by_id(frame_id: UUID) -> FrameView:
    return (await Frame.get(id=frame_id)).to_view()


async def get_by_subtask_id(subtask_id: UUID) -> FrameView:
    frame = await Frame.get(subtasks__id=subtask_id)
    return FrameView.from_orm(frame)


async def get_not_running() -> List[Frame]:
    return await Frame.all().filter(finished=False, running=False).select_for_update()


async def save_result(frame_id: UUID, file: UploadFile, settings: Settings) -> None:
    path = os.path.join(settings.subtask_dir, frame_id.hex + ".exr")
    await save_file(path, file)


async def create(frame: FrameCreate) -> FrameView:
    frame_db = Frame(**frame.dict())
    await frame_db.save()
    return FrameView.from_orm(frame_db)


def __to_view_list(frames: List[Frame]) -> List[FrameView]:
    views: List[FrameView] = []
    for frame in frames:
        views.append(frame.to_view())
    return views
