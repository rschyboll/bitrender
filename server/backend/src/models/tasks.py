from models import BaseModel
from tortoise.fields.data import IntField, TextField


class Task(BaseModel):
    name = TextField()

    engine = TextField()
    samples = IntField()
