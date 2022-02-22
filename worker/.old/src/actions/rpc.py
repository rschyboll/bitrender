import asyncio
from typing import Any

from fastapi_websocket_rpc import WebSocketRpcClient
from fastapi_websocket_rpc.rpc_channel import RpcChannel

from app.action import Action
from config import URL, Settings
from services import RPCCall, RPCClient


class RPC(Action[None]):
    critical = True
    background = False

    def __init__(self, settings: Settings, urls: URL, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls
        self.connected = False

    async def on_connect(self, channel: RpcChannel) -> None:
        self.connected = True

    async def on_disconnect(self, channel: RpcChannel) -> None:
        self.connected = False

    async def _start(self) -> None:
        headers = [("token", self.settings.token)]
        self.state.rpc_client = WebSocketRpcClient(
            self.urls.websocket,
            RPCClient(self),
            extra_headers=headers,
            keep_alive=1,
            on_connect=[self.on_connect],
            on_disconnect=[self.on_disconnect],
        )
        self.state.rpc_call = RPCCall(self.state.rpc_client)
        await self.state.rpc_client.__aenter__()
        while self.connected:
            await self.check_tasks()
            await asyncio.sleep(0.25)
        print("SERVER DICONNECTED")

    async def check_tasks(self) -> None:
        running = self.running.copy()
        for action, task in running.items():
            if task.done():
                await task
                self.running.pop(action)
                self.finished.append(action)

    async def _local_rollback(self) -> None:
        await self._rollback()

    async def _rollback(self) -> None:
        if self.state.rpc_client is not None:
            await self.state.rpc_client.__aexit__()
            self.state.rpc_client = None
            self.state.rpc_call = None
