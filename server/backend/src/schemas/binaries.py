from uuid import UUID

from pydantic import BaseModel


class BinaryCreate(BaseModel):
    version: str
    url: str


class BinaryView(BaseModel):
    id: UUID
    version: str
    url: str

    class Config:
        orm_mode = True
