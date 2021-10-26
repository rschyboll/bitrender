import uvicorn
from fastapi import FastAPI, Header
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint

# Methods to expose to the clients
class ConcatServer(RpcMethodsBase):  # type: ignore
    async def concat(self, a: str = "", b: str = "") -> str:
        return a + b


async def on_connect(channel, id: str = Header(...)) -> None:
    print(endpoint.manager.active_connections[0])


if __name__ == "__main__":
    # Init the FAST-API app
    app = FastAPI()
    # Create an endpoint and load it with the methods to expose
    endpoint = WebsocketRPCEndpoint(ConcatServer(), on_connect=[on_connect])
    # add the endpoint to the app
    endpoint.register_route(app, "/ws")

    # Start the server itself
    uvicorn.run(app, host="0.0.0.0", port=9000)
