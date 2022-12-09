import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:8123"]
fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
app = socketio.ASGIApp(socketio_server=sio, socketio_path="/socket.io")


fastapi_app.mount("/ws", app)


@sio.on("join")
async def handle_join(sid, *args, **kwargs):
    await sio.emit("lobby", "User joined")


@sio.on("test")
async def test(sid, *args, **kwargs):
    await sio.emit("hey", "joe")


if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8123)
