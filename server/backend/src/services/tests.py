import asyncio
import datetime

from fastapi_websocket_rpc import RpcChannel

from schemas.tests import TestUpdate, TestCreate
from storage import tests as TestStorage


class TestsService:
    async def test_status(self, value: int) -> None:
        test_update = TestUpdate(samples=value)
        await TestStorage.update(test_update)

    async def test_error(self) -> None:
        test_update = TestUpdate(error=True)
        await TestStorage.update(test_update)

    async def test_success(self) -> None:
        test_update = TestUpdate(end_time=datetime.datetime.now())
        await TestStorage.update(test_update)


class TestsCall:
    @staticmethod
    async def test_worker(channel: RpcChannel) -> None:
        start_time = datetime.datetime.now()
        test = TestCreate(worker_id=channel.id, start_time=start_time)
        await TestStorage.create(test)
        asyncio.create_task(channel.other.test())
