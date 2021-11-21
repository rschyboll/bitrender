from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntField, TextField
from tortoise.fields.relational import ReverseRelation

from models import BaseModel

if TYPE_CHECKING:
    from models.frames import Frame
else:
    Frame = object


class Task(BaseModel):
    name = TextField()
    samples = IntField()
    start_frame = IntField()
    end_frame = IntField()
    resolution_x = IntField()
    resolution_y = IntField()

    finished = BooleanField(default=False)

    frames: ReverseRelation[Frame]
