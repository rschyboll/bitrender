import asyncio
from typing import Any

from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase, WebSocketRpcClient

from actions.test import Test
from app.action import Action
from config import URL, Settings
from core.rpc_call import RPCCall


class RPC(Action[None]):
    critical = True
    background = False

    def __init__(self, settings: Settings, urls: URL, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls

    async def _start(self) -> None:
        headers = [("token", self.settings.token)]
        async with WebSocketRpcClient(
            self.urls.websocket, RPCClient(self), extra_headers=headers, keep_alive=1
        ) as client:
            await client.wait_on_rpc_ready()
            while True:
                await self.check_tasks()
                await asyncio.sleep(0.25)

    async def check_tasks(self) -> None:
        for action, task in self.running.items():
            if task.done():
                if isinstance(action, Test):
                    pass

    async def test(self, channel: RpcChannel) -> None:
        rpc_call = RPCCall(self.settings, channel)
        await self._start_subaction(Test, rpc_call=rpc_call)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class RPCClient(RpcMethodsBase):
    def __init__(self, rpc: RPC):
        super().__init__()
        self.rpc = rpc

    async def test(self) -> None:
        await self.rpc.test(self.channel)
