from tortoise.fields.data import IntField, DatetimeField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.workers import Worker


class Test(BaseModel):
    date = DatetimeField()
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")
    samples = IntField(null=True)
    progress = IntField(default=0)
