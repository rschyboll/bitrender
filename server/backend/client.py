import asyncio
from typing import Any
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjFmMzM5M2UxNTA4NDQ4Y2ZhMGQ0MjYxMTIwOTA4YjA1IiwibmFtZSI6InRlc3QifQ.jsQPd8k9uzn3dIDs_ewTM3q9LWhcLVdlVf5NTBKm1DI"


class RPCServer(RpcMethodsBase):
    async def concat(self, a: str, b: str) -> str:
        print("PING")
        print(self.channel.id)
        return a + b


async def run_client(uri: str) -> None:
    async with WebSocketRpcClient(
        uri, RpcMethodsBase(), extra_headers=[("token", TOKEN)]
    ) as client:
        while True:
            response = await client.other.concat(a="hello", b=" world")
            # print result
            print(response.result)  # will print "hello world"
            await asyncio.sleep(1)


# run the client until it completes interaction with server
asyncio.get_event_loop().run_until_complete(run_client("ws://localhost:8000/ws"))
