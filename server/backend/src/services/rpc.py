import asyncio
from typing import Optional
from fastapi import WebSocket, Depends, APIRouter
from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase, WebsocketRPCEndpoint

from schemas.workers import WorkerView
from core import worker as WorkerCore
from services import channels as ChannelService
from storage import tests as TestStorage

router = APIRouter()


class RPCServer(RpcMethodsBase):
    async def test_status(self, value: int) -> None:
        asyncio.create_task(RPCCall.test_worker(self.channel))


class RPCCall:
    @staticmethod
    async def test_worker(channel: RpcChannel) -> None:
        await channel.other.test()


async def on_connect(channel: RpcChannel) -> None:
    ChannelService.add(channel, channel.id)
    test = await TestStorage.get_latest(channel.id)
    if test is None:
        asyncio.create_task(RPCCall.test_worker(channel))


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
        await endpoint.main_loop(websocket, channel_id=worker.id)
