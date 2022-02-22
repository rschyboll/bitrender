from typing import List, Optional

from fastapi import Depends, Header, HTTPException, WebSocket

from core import channel as ChannelCore
from core import jwt as JWTCore
from errors.db import RecordNotFound
from models import Worker


def get_token_data(token: Optional[str] = Header(None)) -> JWTCore.JWTData:
    if token is None:
        raise HTTPException(status_code=400)
    return JWTCore.decode_jwt(token)


async def get_current_worker(data: JWTCore.JWTData = Depends(get_token_data)) -> Worker:
    try:
        worker = await Worker.get_by_id(data["id"])
        if data["name"] == worker.name:
            return worker
        raise HTTPException(status_code=400)
    except RecordNotFound as error:
        raise HTTPException(status_code=400) from error


async def get_active_worker(worker: Worker = Depends(get_current_worker)) -> Worker:
    if not worker.active:
        raise HTTPException(status_code=400)
    return worker


async def ws_active_worker(
    websocket: WebSocket, token: Optional[str] = Header(None)
) -> Optional[Worker]:
    try:
        token_data = get_token_data(token)
        current_worker = await get_current_worker(token_data)
        return await get_active_worker(current_worker)
    except HTTPException:
        await websocket.close()
    return None


async def filter_connected(workers: List[Worker]) -> List[Worker]:
    connected_workers: List[Worker] = []
    channels = ChannelCore.connected()
    for worker in workers:
        if worker.id in channels:
            connected_workers.append(worker)
    return connected_workers
