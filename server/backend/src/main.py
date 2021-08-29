import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import binaries, tasks, workers
from storage import init_db

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks.router)
app.include_router(workers.router)
app.include_router(binaries.router)

init_db(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
