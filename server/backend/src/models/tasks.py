from tortoise.fields.data import IntField, TextField

from models import BaseModel


class Task(BaseModel):
    name = TextField()

    engine = TextField()
    samples = IntField()
