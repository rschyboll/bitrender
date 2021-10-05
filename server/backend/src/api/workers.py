from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect

from core import jwt
from schemas.workers import WorkerCreate, WorkerUpdate, WorkerView
from storage import workers as WorkerStorage
from services.workers import connection_manager

router = APIRouter(prefix="/workers")


async def get_current_worker(token: Optional[str] = Header(None)) -> WorkerView:
    if token is None:
        raise HTTPException(status_code=401, detail="No authorization token")
    worker_name, worker_id = jwt.decode_jwt(token)
    worker = await WorkerStorage.get_by_id(UUID(worker_id))
    if worker is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if worker_name == worker.name:
        return worker
    raise HTTPException(status_code=401, detail="Corrupted token")


async def get_active_worker(
    current_worker: WorkerView = Depends(get_current_worker),
) -> WorkerView:
    if current_worker.active:
        return current_worker
    raise HTTPException(status_code=401, detail="Not active")


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
    return jwt.create_jwt({"name": name, "id": worker_view.id.hex})


@router.post("/activate")
async def activate(worker_id: UUID = Body(...), status: bool = Body(...)) -> WorkerView:
    worker_update = WorkerUpdate(id=worker_id, active=status)
    return await WorkerStorage.update(worker_update)


@router.delete("/deregister")
async def deregister(current_worker: WorkerView = Depends(get_current_worker)) -> None:
    await WorkerStorage.delete(current_worker.id)


@router.websocket("/workers/ws")
async def websocket_endpoint(
    websocket: WebSocket, active_worker: WorkerView = Depends(get_active_worker)
) -> None:
    await connection_manager.connect(websocket, active_worker.id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(data, active_worker.id)
    except WebSocketDisconnect:
        connection_manager.disconnect(active_worker.id)
