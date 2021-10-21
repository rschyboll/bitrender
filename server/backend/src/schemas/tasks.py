from enum import Enum
from typing import Type, TypeVar
from uuid import UUID

from fastapi import File, Form, UploadFile
from pydantic import BaseModel

TASKCREATE = TypeVar("TASKCREATE", bound="TaskCreate")


class TaskCreate(BaseModel):
    file: UploadFile
    samples: int

    @classmethod
    def as_form(
        cls: Type[TASKCREATE],
        file: UploadFile = File(...),
        samples: int = Form(...),
    ) -> TASKCREATE:
        return cls(file=file, samples=samples)


class TaskView(BaseModel):
    id: UUID
    name: str
    samples: int

    class Config:
        orm_mode = True
