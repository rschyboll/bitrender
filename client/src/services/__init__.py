from typing import Any

from fastapi_websocket_rpc import RpcChannel, RpcMethodsBase

from app.action import Action
from services.test import TestCall, TestClient


class RPCClient(RpcMethodsBase, TestClient):
    def __init__(self, action: Action[Any]):
        self.action = action
        RpcMethodsBase.__init__(self)
        TestClient.__init__(self, action)


class RPCCall(TestCall):
    def __init__(self, channel: RpcChannel):
        super().__init__(channel)
        self.channel = channel
