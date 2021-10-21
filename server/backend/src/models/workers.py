from tortoise.fields.data import BooleanField, DatetimeField, IntField, TextField

from models import BaseModel


class Worker(BaseModel):
    name = TextField()
    register_date = DatetimeField()

    active = BooleanField(default=False)
    test_time = IntField(null=True, default=None)
