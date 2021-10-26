from tortoise.fields.data import FloatField, IntField, TextField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.tasks import Task


class SubTask(BaseModel):
    frame = IntField()
    seed = IntField()
    time_limit = IntField()
    max_samples = IntField()
    rendered_samples = IntField(null=True)

    task: ForeignKeyRelation[Task] = ForeignKeyField(
        "models.Tournament", related_name="events"
    )
