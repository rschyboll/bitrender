from tortoise.fields.data import BooleanField, DatetimeField, FloatField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.workers import Worker


class Test(BaseModel):
    start_time = DatetimeField()
    end_time = DatetimeField(null=True)

    sync_time = FloatField(null=True)
    render_time = FloatField(null=True)

    error = BooleanField(default=False)
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")
