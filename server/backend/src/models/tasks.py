from tortoise.fields.data import IntField, TextField

from models import BaseModel


class Task(BaseModel):
    name = TextField()
    samples = IntField()
    start_frame = IntField()
    end_frame = IntField()
    resolution_x = IntField()
    resolution_y = IntField()
