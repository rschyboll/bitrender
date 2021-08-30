from typing import List, Optional
from uuid import UUID

from config import get_settings
from models.workers import Worker
from schemas.workers import WorkerCreate, WorkerUpdate, WorkerView

settings = get_settings()


async def create(worker: WorkerCreate) -> WorkerView:
    worker_db = Worker(**worker.dict())
    await worker_db.save()
    return WorkerView.from_orm(worker_db)


async def get() -> List[WorkerView]:
    workers = await Worker.all()
    worker_views: List[WorkerView] = []
    for worker in workers:
        worker_views.append(WorkerView.from_orm(worker))
    return worker_views


async def get_by_id(worker_id: UUID) -> Optional[WorkerView]:
    worker = await Worker.get(id=worker_id)
    return WorkerView.from_orm(worker)


async def update(worker_update: WorkerUpdate) -> WorkerView:
    worker = await Worker.get(id=worker_update.id)
    worker.update_from_dict(worker_update.dict(exclude_unset=True, exclude={"id"}))
    await worker.save()
    return WorkerView.from_orm(worker)


async def delete(worker_id: UUID) -> None:
    worker = await Worker.get(id=worker_id)
    await worker.delete()
