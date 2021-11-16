from typing import List
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from models.frames import Frame
from schemas.frames import FrameCreate, FrameView


async def create(frame: FrameCreate) -> FrameView:
    frame_db = Frame(**frame.dict())
    await frame_db.save()
    return FrameView.from_orm(frame_db)


async def get() -> List[FrameView]:
    frames = await Frame.all()
    frame_views: List[FrameView] = []
    for frame in frames:
        frame_views.append(FrameView.from_orm(frame))
    return frame_views


async def get_by_id(frame_id: UUID) -> FrameView:
    frame_db = await Frame.get(id=frame_id)
    return FrameView.from_orm(frame_db)


async def get_latest() -> FrameView:
    frame_db = await Frame.all().order_by("-id").first()
    if frame_db is None:
        raise DoesNotExist
    return FrameView.from_orm(frame_db)


async def delete(frame_id: UUID) -> None:
    frame_db = await Frame.get(id=frame_id)
    await frame_db.delete()
