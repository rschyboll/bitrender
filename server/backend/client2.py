"""
This example (along with 'examples/bidirectional_server_example.py') 
builds on top of the simple example and adds- calls from the server to the client as well
"""
import asyncio
from os import wait
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient, logger

# set fastapi-websocket-rpc logging to DEBUG
logger.logging_config.set_mode(logger.LoggingModes.UVICORN, logger.logging.DEBUG)

PORT = 9000


# Methods to expose to the clients
class WaitingClient(RpcMethodsBase):
    def __init__(self):
        super().__init__()

    async def send_file(self, data):
        print(len(data))


async def run_client(uri):
    async with WebSocketRpcClient(uri, WaitingClient()) as client:
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    # run the client until it completes interaction with server
    asyncio.get_event_loop().run_until_complete(run_client(f"ws://localhost:{PORT}/ws"))
