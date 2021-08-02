from typing import Type, TypeVar
from enum import Enum

from fastapi import Form, File, UploadFile
from pydantic import BaseModel, UUID4

# pylint: disable=invalid-name
T = TypeVar("T", bound="TaskIn")
# pylint: enable=invalid-name


class Engines(str, Enum):
    CYCLES = "cycles"
    EEVEE = "eevee"


class TaskIn(BaseModel):
    file: UploadFile
    engine: Engines
    samples: int

    @classmethod
    def as_form(
        cls: Type[T],
        file: UploadFile = File(...),
        engine: Engines = Form(...),
        samples: int = Form(...),
    ) -> T:
        return cls(file=file, engine=engine, samples=samples)


class TaskView(BaseModel):
    id: UUID4
    name: str
    engine: str
    samples: int

    class Config:
        orm_mode = True
