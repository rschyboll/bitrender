from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from schemas.workers import WorkerView


class TestView(BaseModel):
    id: UUID

    date: datetime
    worker: WorkerView
    seconds: int

    class Config:
        orm_mode = True
