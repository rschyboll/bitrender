import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, WebSocket
from fastapi_websocket_rpc import RpcChannel, WebsocketRPCEndpoint

from core import channel as ChannelCore
from core import task as TaskCore
from core import worker as WorkerCore
from models import Test, Worker
from services.tasks import TasksService
from services.tests import TestsCall, TestsService

router = APIRouter()


class RPCService(TestsService, TasksService):
    pass


class RPCCall(TestsCall):
    pass


async def on_connect(channel: RpcChannel) -> None:
    ChannelCore.add(channel, channel.id)
    test = await Test.get_latest(channel.id)
    if test is None or test.render_time is None:
        await RPCCall.test_worker(channel)
    else:
        asyncio.create_task(TaskCore.distribute_tasks())


async def on_disconnect(channel: RpcChannel) -> None:
    ChannelCore.remove(channel.id)
    test = await Test.get_latest(channel.id)
    worker = await Worker.get_by_id(channel.id)
    if test is not None and test.render_time is None:
        await (await Test.get_by_id(channel.id)).delete(test.id)
        worker.test = None
    worker.subtask = None
    await worker.save()


endpoint = WebsocketRPCEndpoint(
    RPCService(),
    on_connect=[on_connect],
    on_disconnect=[on_disconnect],
)


@router.websocket("/ws")
async def websocket_rpc_endpoint(
    websocket: WebSocket,
    worker: Optional[Worker] = Depends(WorkerCore.ws_active_worker),
) -> None:
    if worker is not None:
        await endpoint.main_loop(websocket, channel_id=worker.id)
