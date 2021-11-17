from typing import TYPE_CHECKING

from tortoise.fields.data import DateField, IntField, TextField
from tortoise.fields.relational import ReverseRelation

from models import BaseModel

if TYPE_CHECKING:
    from models.frames import Frame
else:
    Frame = object


class Task(BaseModel):
    name = TextField()
    date = DateField()
    samples = IntField()
    start_frame = IntField()
    end_frame = IntField()
    resolution_x = IntField()
    resolution_y = IntField()
    frames: ReverseRelation[Frame]
