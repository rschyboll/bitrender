from typing import List
from uuid import UUID

from models.frames import Frame
from schemas.frames import FrameCreate, FrameUpdate, FrameView


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


async def get_not_running() -> List[FrameView]:
    frames = await Frame.all().filter(finished=False, running=False).select_for_update()
    frame_views: List[FrameView] = []
    for frame in frames:
        frame_views.append(FrameView.from_orm(frame))
    return frame_views


async def update(frame_update: FrameUpdate) -> FrameView:
    frame_db = await Frame.all().select_for_update().get(id=frame_update.id)
    frame_db.update_from_dict(frame_update.dict(exclude_unset=True, exclude={"id"}))
    await frame_db.save()
    return FrameView.from_orm(frame_db)


async def delete(frame_id: UUID) -> None:
    frame_db = await Frame.get(id=frame_id)
    await frame_db.delete()
