from typing import Dict, List
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.__active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, worker_id: UUID) -> None:
        await websocket.accept()
        self.__active_connections[worker_id] = websocket

    async def disconnect(self, worker_id: UUID) -> None:
        self.__active_connections.pop(worker_id)

    async def send_personal_message(self, message: str, worker_id: UUID) -> None:
        await self.__active_connections[worker_id].send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.__active_connections.values():
            await connection.send_text(message)

    @property
    def connected_workers(self) -> List[UUID]:
        return list(self.__active_connections.keys())


connection_manager = ConnectionManager()
