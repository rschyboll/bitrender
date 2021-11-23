from typing import Type, TypeVar

from fastapi import File, Form, UploadFile

from .base import BaseCreate, BaseView

TASKCREATE = TypeVar("TASKCREATE", bound="TaskCreate")


class TaskView(BaseView):
    name: str
    samples: int
    start_frame: int
    end_frame: int
    resolution_x: int
    resolution_y: int

    finished: bool

    class Config:
        orm_mode = True


class TaskCreate(BaseCreate):
    file: UploadFile
    samples: int
    start_frame: int
    end_frame: int
    resolution_x: int
    resolution_y: int

    @classmethod
    def as_form(
        cls: Type[TASKCREATE],
        file: UploadFile = File(...),
        samples: int = Form(...),
        start_frame: int = Form(...),
        end_frame: int = Form(...),
        resolution_x: int = Form(...),
        resolution_y: int = Form(...),
    ) -> TASKCREATE:
        return cls(
            file=file,
            samples=samples,
            start_frame=start_frame,
            end_frame=end_frame,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
        )
