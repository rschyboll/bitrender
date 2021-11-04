from tortoise.fields.data import IntField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.tasks import Task


class SubTask(BaseModel):
    frame = IntField()
    seed = IntField()
    time_limit = IntField()
    max_samples = IntField()
    rendered_samples = IntField(null=True)

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
    progress = IntField(default=0)
