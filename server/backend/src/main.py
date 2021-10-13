import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import binaries, tasks, workers
from storage import register_db, migrate

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


def __create_app() -> FastAPI:
    return FastAPI()


def __init_routers(__app: FastAPI) -> None:
    __app.include_router(tasks.router)
    __app.include_router(workers.router)
    __app.include_router(binaries.router)


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
