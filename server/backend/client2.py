import asyncio
from typing import Any
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRhMDljN2Q3ZTI5MzQwZmI5NDFkNzdjZjIzMTAzMzZiIiwibmFtZSI6InRlc3QifQ.M0wRxqkXDB4DCLcTnNNBZ32PD3MiiTd-2mB5TbP7ERY"


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
