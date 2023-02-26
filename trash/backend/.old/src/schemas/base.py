from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseView(BaseModel):
    id: UUID
    create_date: datetime

    class Config:
        orm_mode = True


class BaseCreate(BaseModel):
    pass
