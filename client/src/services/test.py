from typing import Any, TYPE_CHECKING

from actions.test import Test
from app.action import Action

if TYPE_CHECKING:
    from services import RPCClient
else:
    RPCClient = object


class TestClient:
    def __init__(self, action: Action[Any]):
        super().__init__()
        self.action = action

    async def test(self) -> None:
        await self.action.start_background_subaction(Test)


class TestCall:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client

    async def test_success(self, sync_time: float, render_time: float) -> None:
        await self.rpc_client.channel.other.test_success(
            sync_time=sync_time,
            render_time=render_time,
        )

    async def test_error(self) -> None:
        await self.rpc_client.channel.other.test_error()
