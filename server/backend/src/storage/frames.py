from typing import List
from uuid import UUID

from tortoise.functions import Count, Min
from tortoise.query_utils import Prefetch
from tortoise.queryset import Q
from tortoise.expressions import Subquery

from models.frames import Frame
from models.subtasks import Subtask
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


async def get_not_finished() -> List[FrameView]:
    frames = await Frame.filter(finished=False).select_for_update()
    frame_views: List[FrameView] = []
    for frame in frames:
        frame_views.append(FrameView.from_orm(frame))
    return frame_views


async def get_not_running() -> List[FrameView]:
    subtasks_query = (
        Frame.all()
        .annotate(total_amount=Count("subtasks", _filter=Q(subtasks__finished=False)))
        .filter(total_amount=0)
        .group_by("id")
        .values_list("id", flat=True)
    )

    test3 = await subtasks_query

    test2 = await (
        Frame.all()
        .annotate(not_running=Subquery(subtasks_query))
        .filter(id__in=subtasks_query)
    )

    test = (
        await Frame.all()
        .annotate(not_running=Subquery(subtasks_query))
        .filter(task__id__isnull=False, finished=False)
        .order_by("task__date", "id")
    )

    frames_ids = await (
        Frame.all()
        .annotate(not_running=Count("subtasks", _filter=Q(subtasks__finished=False)))
        .annotate(task_date=Min("task__date"))
        .filter(task__id__isnull=False)
        .filter(not_running=0)
        .filter(finished=False)
        .order_by("task_date", "id")
    )
    frame_views: List[FrameView] = []
    for frame in frames:
        frame_views.append(FrameView.from_orm(frame))
    return frame_views


async def delete(frame_id: UUID) -> None:
    frame_db = await Frame.get(id=frame_id)
    await frame_db.delete()
