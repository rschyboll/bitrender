from fastapi import FastAPI, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.post("/task/new")
async def root(file: bytes = File(...)):
    print(file)
