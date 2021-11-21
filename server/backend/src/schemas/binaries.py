from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BinaryView(BaseModel):
    id: UUID
    create_date: datetime
    version: str
    url: str

    class Config:
        orm_mode = True


class BinaryCreate(BaseModel):
    version: str
    url: str
