import asyncio
import datetime

from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase

from schemas.tests import TestCreate, TestUpdate
from storage import tests as TestStorage


class TestsService(RpcMethodsBase):
    def __init__(self) -> None:
        super().__init__()
        self._channel: RpcChannel

    async def test_error(self) -> None:
        test = await TestStorage.get_latest(self._channel.id)
        if test is not None:
            test_update = TestUpdate(id=test.id, error=True)
            await TestStorage.update(test_update)

    async def test_success(self, render_time: float, sync_time: float) -> None:
        test = await TestStorage.get_latest(self._channel.id)
        if test is not None:
            test_update = TestUpdate(
                id=test.id,
                end_time=datetime.datetime.now(),
                render_time=render_time,
                sync_time=sync_time,
            )
            await TestStorage.update(test_update)


class TestsCall:
    @staticmethod
    async def test_worker(channel: RpcChannel) -> None:
        start_time = datetime.datetime.now()
        test = TestCreate(worker_id=channel.id, start_time=start_time)
        await TestStorage.create(test)
        asyncio.create_task(channel.other.test())
