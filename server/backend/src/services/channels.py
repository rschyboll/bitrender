from typing import Dict, List, Optional
from uuid import UUID

from fastapi_websocket_rpc import RpcChannel

__active_connections: Dict[UUID, RpcChannel] = {}


def add(channel: RpcChannel, worker_id: UUID) -> None:
    __active_connections[worker_id] = channel


def remove(worker_id: UUID) -> None:
    if worker_id in __active_connections:
        __active_connections.pop(worker_id)


def get(worker_id: UUID) -> Optional[RpcChannel]:
    if worker_id in __active_connections:
        return __active_connections[worker_id]
    return None


def connected_workers() -> List[UUID]:
    return list(__active_connections.keys())
