from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from core import jwt as JWTCore
from core import worker as WorkerCore
from models import Worker
from schemas import WorkerCreate, WorkerView

router = APIRouter(prefix="/workers")


@router.get("/")
async def get_workers() -> List[WorkerView]:
    return await Worker.get_all(True)


@router.post("/register")
async def register(name: str = Body(...)) -> str:
    worker = await Worker.make(name=name)
    return JWTCore.create_jwt({"name": name, "id": worker.id})


@router.post("/activate")
async def activate(worker_id: UUID = Body(...), status: bool = Body(...)) -> WorkerView:
    worker = await Worker.get_by_id(worker_id)
    worker.active = status
    await worker.save()
    return worker.to_view()


@router.delete("/deregister")
async def deregister(worker: Worker = Depends(WorkerCore.get_current_worker)) -> None:
    await worker.delete()
