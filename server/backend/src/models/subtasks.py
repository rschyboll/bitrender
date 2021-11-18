from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import (
    ForeignKeyField,
    ForeignKeyRelation,
    ReverseRelation,
)

from models import BaseModel
from models.frames import Frame

if TYPE_CHECKING:
    from models.workers import Worker
else:
    Worker = object


class Subtask(BaseModel):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")
    seed = IntField()
    time_limit = IntField()
    max_samples = IntField()
    rendered_samples = IntField(null=True)
    assigned = BooleanField(default=False)
    finished = BooleanField(default=False)
    worker = ReverseRelation[Worker]
