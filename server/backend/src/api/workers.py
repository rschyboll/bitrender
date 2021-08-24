from datetime import datetime
from typing import List, Optional
from uuid import UUID

from core import workers as WorkerCore
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from schemas.workers import WorkerCreate, WorkerUpdate, WorkerView
from storage import workers as WorkerStorage


class ConnectionManager:
    def __init__(self) -> None:
        self.__active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.__active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.__active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.__active_connections:
            await connection.send_text(message)


connection_manager = ConnectionManager()
router = APIRouter(prefix="/workers")


async def get_current_worker(token: Optional[str] = Header(None)) -> WorkerView:
    if token is None:
        raise HTTPException(status_code=401, detail="No authorization token")
    worker_name, worker_id = WorkerCore.decode_jwt(token)
    worker = await WorkerStorage.get_by_id(worker_id)
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
    return WorkerCore.create_jwt(
        worker_name=name,
        worker_id=worker_view.id,
    )


@router.post("/activate")
async def activate(worker_id: UUID = Body(...), status: bool = Body(...)) -> WorkerView:
    worker_update = WorkerUpdate(id=worker_id, active=status)
    return await WorkerStorage.update(worker_update)


@router.delete("/deregister")
async def deregister(current_worker: WorkerView = Depends(get_current_worker)) -> None:
    await WorkerStorage.delete(current_worker.id)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
