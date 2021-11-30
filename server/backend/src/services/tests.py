import asyncio

from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase

from core import task as TaskCore
from models import Test, Worker
from schemas import TestCreate


class TestsService(RpcMethodsBase):
    async def test_error(self) -> None:
        worker = await Worker.get_by_id(self.channel.id)
        if worker.test is not None:
            test = await worker.test
            if test is not None:
                test.error = True
                await test.save()
                return
        await TestsCall.test_worker(self.channel)

    async def test_success(self, render_time: float, sync_time: float) -> None:
        worker = await Worker.get_by_id(self.channel.id)
        if worker.test is not None:
            test = await worker.test
            if test is not None:
                test.render_time = render_time
                test.sync_time = sync_time
                await test.save()
                asyncio.create_task(TaskCore.distribute_tasks())
                return
        await TestsCall.test_worker(self.channel)


class TestsCall:
    @staticmethod
    async def test_worker(channel: RpcChannel) -> None:
        worker = await Worker.get_by_id(channel.id)
        worker.test = await Test.make(worker_id=channel.id)
        await worker.save()
        asyncio.create_task(channel.other.test())
