import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import services
from api import binaries, subtasks, tasks, workers
from storage import migrate, register_db

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


def __create_app() -> FastAPI:
    return FastAPI()


def __init_routers(_app: FastAPI) -> None:
    _app.include_router(tasks.router)
    _app.include_router(workers.router)
    _app.include_router(binaries.router)
    _app.include_router(services.router)
    _app.include_router(subtasks.router)


def __init_middleware(__app: FastAPI) -> None:
    __app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = __create_app()
__init_routers(app)
__init_middleware(app)

register_db(app)


@app.on_event("startup")
async def startup() -> None:
    await migrate()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=os.environ["log_level"])
