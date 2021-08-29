from tortoise.fields.data import BooleanField, DatetimeField, TextField

from models import BaseModel


class Worker(BaseModel):
    name = TextField()

    register_date = DatetimeField()
    active = BooleanField(default=False)
