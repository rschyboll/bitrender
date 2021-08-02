from tortoise.fields.data import TextField, IntField

from models import BaseModel


class Task(BaseModel):
    name = TextField()

    engine = TextField()
    samples = IntField()
