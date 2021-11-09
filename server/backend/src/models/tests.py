from tortoise.fields.data import BooleanField, DatetimeField, IntField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.workers import Worker


class Test(BaseModel):
    start_time = DatetimeField()
    end_time = DatetimeField(null=True)
    samples = IntField(null=True)
    error = BooleanField(default=False)
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")
