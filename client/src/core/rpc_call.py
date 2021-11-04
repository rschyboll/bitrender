from fastapi_websocket_rpc import RpcChannel

from config import Settings


class RPCCall:
    def __init__(self, settings: Settings, channel: RpcChannel):
        self.settings = settings
        self.channel = channel

    async def set_test_progress(self, value: int) -> None:
        pass

    async def set_task_progress(self, value: int) -> None:
        pass
