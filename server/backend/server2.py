import asyncio
import uvicorn
import aiofiles
from fastapi import FastAPI
from fastapi_websocket_rpc import (
    RpcMethodsBase,
    WebsocketRPCEndpoint,
    logger,
    RpcChannel,
)
import random

# Set debug logging
logger.logging_config.set_mode(logger.LoggingModes.UVICORN, logger.logging.WARNING)

# Methods to expose to the clients
class ConcatServer(RpcMethodsBase):
    async def concat(self, a="", b=""):
        # allow client to exit after some time after
        asyncio.create_task(self.channel.other.allow_exit(delay=random.randint(1, 4)))
        # return calculated response
        return a + b


async def on_connect(channel: RpcChannel):
    # Wait a bit
    await asyncio.sleep(1)
    # now tell the client it can start sending us queries
    async with aiofiles.open("../resources/classroom.blend", mode="rb") as f:
        content = await f.read(1024)
        await channel.other.send_file(data=content)


# Init the FAST-API app
app = FastAPI()
# Create an endpoint and load it with the methods to expose
endpoint = WebsocketRPCEndpoint(ConcatServer(), on_connect=[on_connect])
# add the endpoint to the app
endpoint.register_route(app)

# Start the server itself
uvicorn.run(app, host="0.0.0.0", port=9000)
