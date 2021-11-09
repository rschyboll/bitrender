from typing import Any

from fastapi_websocket_rpc import RpcChannel

from actions.test import Test
from app.action import Action


class TestClient:
    def __init__(self, action: Action[Any]):
        super().__init__()
        self.action = action

    async def test(self) -> None:
        await self.action.start_subaction(Test)


class TestCall:
    def __init__(self, channel: RpcChannel):
        self.channel = channel
