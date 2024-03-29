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
    worker = await Worker.get_by_id(channel.id)
    test = await worker.get_test()
    if test is None or test.render_time is None:
        await RPCCall.test_worker(channel)
    else:
        asyncio.create_task(TaskCore.distribute_tasks())


async def on_disconnect(channel: RpcChannel) -> None:
    ChannelCore.remove(channel.id)
    worker = await Worker.get_by_id(channel.id)
    test = await worker.get_test()
    if worker.subtask is not None:
        subtask = await worker.subtask
        if subtask is not None and subtask.test:
            frame = await subtask.frame
            frame.testing = False
            await frame.save()
    if test is not None and test.render_time is None:
        await test.delete()
        worker.test = None
    await __remove_composite_task(worker)
    worker.subtask = None
    worker.composite_task = None
    await worker.save()


async def __remove_composite_task(worker: Worker) -> None:
    if worker.composite_task is not None:
        composite_task = await worker.composite_task
        if composite_task is not None:
            frame = await composite_task.frame
            frame.merging = False
            await frame.save()


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
