from typing import Optional

from fastapi import Depends, Header, HTTPException, WebSocket

from core import jwt as JWTCore
from schemas.workers import WorkerView
from storage import workers as WorkerStorage


def get_token_data(token: Optional[str] = Header(None)) -> JWTCore.JWTData:
    if token is None:
        raise HTTPException(status_code=400)
    return JWTCore.decode_jwt(token)


async def get_current_worker(
    data: JWTCore.JWTData = Depends(get_token_data),
) -> WorkerView:
    worker = await WorkerStorage.get_by_id(data["id"])
    if worker is None:
        raise HTTPException(status_code=400)
    if data["name"] == worker.name:
        return worker
    raise HTTPException(status_code=400)


async def get_active_worker(
    worker: WorkerView = Depends(get_current_worker),
) -> WorkerView:
    if not worker.active:
        raise HTTPException(status_code=400)
    return worker


async def ws_active_worker(
    websocket: WebSocket, token: Optional[str] = Header(None)
) -> Optional[WorkerView]:
    try:
        token_data = get_token_data(token)
        current_worker = await get_current_worker(token_data)
        return await get_active_worker(current_worker)
    except HTTPException:
        await websocket.close()
    return None
