from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from core import jwt as JWTCore
from core import worker as WorkerCore
from schemas.workers import WorkerCreate, WorkerUpdate, WorkerView
from storage import workers as WorkerStorage

router = APIRouter(prefix="/workers")


@router.get("/")
async def get_workers() -> List[WorkerView]:
    return await WorkerStorage.get()


@router.post("/register")
async def register(name: str = Body(...)) -> str:
    worker = WorkerCreate(
        name=name,
        register_date=datetime.now(),
    )
    worker_view = await WorkerStorage.create(worker)
    print(JWTCore.create_jwt({"name": name, "id": worker_view.id}))
    return JWTCore.create_jwt({"name": name, "id": worker_view.id})


@router.post("/activate")
async def activate(worker_id: UUID = Body(...), status: bool = Body(...)) -> WorkerView:
    worker_update = WorkerUpdate(id=worker_id, active=status)
    return await WorkerStorage.update(worker_update)


@router.delete("/deregister")
async def deregister(
    current_worker: WorkerView = Depends(WorkerCore.get_current_worker),
) -> None:
    await WorkerStorage.delete(current_worker.id)
