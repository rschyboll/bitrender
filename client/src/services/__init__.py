from typing import Any

from fastapi_websocket_rpc import RpcMethodsBase

from app.action import Action
from services.test import TestCall, TestClient


class RPCClient(RpcMethodsBase, TestClient):
    def __init__(self, action: Action[Any]):
        self.action = action
        RpcMethodsBase.__init__(self)
        TestClient.__init__(self, action)


class RPCCall(TestCall):
    def __init__(self, rpc_client: RPCClient):
        super().__init__(rpc_client)
        self.channel = rpc_client
