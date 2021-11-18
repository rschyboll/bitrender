from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase, WebsocketRPCEndpoint

from core import channel as ChannelCore
from core import worker as WorkerCore
from schemas.tests import TestCreate
from schemas.workers import WorkerView
from services.tasks import TasksService
from services.tests import TestsCall, TestsService
from storage import tests as TestStorage

router = APIRouter()


class RPCService(TestsService, TasksService):
    pass


class RPCCall(TestsCall):
    pass


async def on_connect(channel: RpcChannel) -> None:
    ChannelCore.add(channel, channel.id)
    test = await TestStorage.get_latest(channel.id)
    if test is None or test.render_time is None or test.sync_time is None:
        await RPCCall.test_worker(channel)


async def on_disconnect(channel: RpcChannel) -> None:
    ChannelCore.remove(channel.id)
    test = await TestStorage.get_latest(channel.id)
    if test is not None and test.end_time is None:
        await TestStorage.delete(test.id)


endpoint = WebsocketRPCEndpoint(
    RPCService(),
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
