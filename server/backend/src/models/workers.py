from models import BaseModel
from tortoise.fields.data import BooleanField, DatetimeField, TextField


class Worker(BaseModel):
    name = TextField()

    register_date = DatetimeField()
    active = BooleanField(default=False)
