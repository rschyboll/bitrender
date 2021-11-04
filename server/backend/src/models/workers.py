from tortoise.fields.data import BooleanField, DatetimeField, TextField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.subtasks import SubTask


class Worker(BaseModel):
    name = TextField()
    register_date = DatetimeField()

    active = BooleanField(default=False)

    task: ForeignKeyRelation[SubTask] = ForeignKeyField(
        "rendering_server.SubTask", null=True
    )
