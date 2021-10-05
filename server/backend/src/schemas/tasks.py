from enum import Enum
from typing import Type, TypeVar
from uuid import UUID

from fastapi import File, Form, UploadFile
from pydantic import BaseModel

TASKCREATE = TypeVar("TASKCREATE", bound="TaskCreate")


class Engines(str, Enum):
    CYCLES = "cycles"
    EEVEE = "eevee"


class TaskCreate(BaseModel):
    file: UploadFile
    engine: Engines
    samples: int

    @classmethod
    def as_form(
        cls: Type[TASKCREATE],
        file: UploadFile = File(...),
        engine: Engines = Form(...),
        samples: int = Form(...),
    ) -> TASKCREATE:
        return cls(file=file, engine=engine, samples=samples)


class TaskView(BaseModel):
    id: UUID
    name: str
    engine: Engines
    samples: int

    class Config:
        orm_mode = True
