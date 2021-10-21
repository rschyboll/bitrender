from typing import Dict, Optional, Any
from uuid import UUID

from fastapi import Depends, Header, HTTPException, WebSocket, status

from core.jwt import JWTData, decode_jwt
from schemas.workers import WorkerView
from schemas.actions import Action, ActionType
from storage import workers as WorkerStorage


class ConnectionManager:
    def __init__(self) -> None:
        self.__active_connections: Dict[UUID, WebSocket] = {}

    def connect(self, websocket: WebSocket, worker_id: UUID) -> None:
        self.__active_connections[worker_id] = websocket

    def disconnect(self, worker_id: UUID) -> None:
        self.__active_connections.pop(worker_id)


connection_manager = ConnectionManager()


async def token_data(token: Optional[str] = Header(None)) -> JWTData:
    if token is None:
        raise HTTPException(status_code=401, detail="No authorization token")
    return decode_jwt(token)


async def current_worker(data: JWTData = Depends(token_data)) -> WorkerView:
    worker = await WorkerStorage.get_by_id(data["id"])
    if worker is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if data["name"] == worker.name:
        return worker
    raise HTTPException(status_code=401, detail="Corrupted token")


async def active_worker(
    websocket: WebSocket, worker: WorkerView = Depends(current_worker)
) -> Optional[WorkerView]:
    if not worker.active:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    return worker


async def on_connect(websocket: WebSocket, worker: WorkerView) -> None:
    await websocket.accept()
    connection_manager.connect(websocket, worker.id)
    if worker.test_time is None:
        action = Action(type=ActionType.TEST)
        await websocket.send_json(action.to_dict())


async def on_receive(worker: WorkerView, data: Any) -> None:
    print(data)


async def on_disconnect(websocket: WebSocket, worker: WorkerView) -> None:
    await websocket.close()
    connection_manager.disconnect(worker.id)
