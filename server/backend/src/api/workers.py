from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect

from core import jwt
from schemas.workers import WorkerCreate, WorkerUpdate, WorkerView
from services import workers as WorkerService
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
    return jwt.create_jwt({"name": name, "id": worker_view.id})


@router.post("/activate")
async def activate(worker_id: UUID = Body(...), status: bool = Body(...)) -> WorkerView:
    worker_update = WorkerUpdate(id=worker_id, active=status)
    return await WorkerStorage.update(worker_update)


@router.delete("/deregister")
async def deregister(
    current_worker: WorkerView = Depends(WorkerService.current_worker),
) -> None:
    await WorkerStorage.delete(current_worker.id)


@router.websocket("/workers/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    worker: Optional[WorkerView] = Depends(WorkerService.active_worker),
) -> None:
    if worker is None:
        return
    try:
        await WorkerService.on_connect(websocket, worker)
        while True:
            data = await websocket.receive()
            await WorkerService.on_receive(worker, data)
    except (WebSocketDisconnect, RuntimeError):
        await WorkerService.on_disconnect(websocket, worker)
