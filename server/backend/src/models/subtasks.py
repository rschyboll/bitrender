from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.frames import Frame


class Subtask(BaseModel):
    frame: ForeignKeyRelation[Frame] = ForeignKeyField("rendering_server.Frame")
    seed = IntField()
    time_limit = IntField()
    max_samples = IntField()
    rendered_samples = IntField(null=True)
    finished = BooleanField(default=False)
