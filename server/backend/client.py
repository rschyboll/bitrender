import asyncio
from typing import Any
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
from server import ConcatServer


class RCPClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = WebSocketRpcClient(uri, RpcMethodsBase())

    async def __aenter__(self) -> None:
        await self.client.__aenter__()

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.client.__aexit__(args, kwargs)

    async def concat(self, abc: str, bca: str) -> str:
        response = self.client.other.concat(a=abc, b=bca)
        if isinstance(response, str):
            return response
        raise Exception()


async def run_client(uri: str) -> None:
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        # call concat on the other side
        response = await client.other.concat(a="hello", b=" world")
        # print result
        print(response.result)  # will print "hello world"


# run the client until it completes interaction with server
asyncio.get_event_loop().run_until_complete(run_client("ws://localhost:9000/ws"))
