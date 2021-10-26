from typing import Optional
from fastapi import WebSocket, Depends, APIRouter
from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase, WebsocketRPCEndpoint

from schemas.workers import WorkerView
from core import worker as WorkerCore
from services import channels as ChannelService

router = APIRouter()


class RPCServer(RpcMethodsBase):
    async def concat(self, a: str, b: str) -> str:
        print("PING")
        print(self.channel.id)
        return a + b


class RPCCall:
    async def ping(self) -> None:
        print("PONG")


async def on_connect(channel: RpcChannel) -> None:
    ChannelService.add(channel, channel.id)


async def on_disconnect(channel: RpcChannel) -> None:
    ChannelService.remove(channel.id)


endpoint = WebsocketRPCEndpoint(
    RPCServer(),
    on_connect=[on_connect],
    on_disconnect=[on_disconnect],
)


@router.websocket("/ws")
async def websocket_rpc_endpoint(
    websocket: WebSocket,
    worker: Optional[WorkerView] = Depends(WorkerCore.ws_active_worker),
) -> None:
    if worker is not None:
        print(worker.id)
        await endpoint.main_loop(websocket, channel_id=worker.id)
