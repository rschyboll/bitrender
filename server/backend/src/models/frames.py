from tortoise.fields.data import BooleanField, IntField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel
from models.tasks import Task


class Frame(BaseModel):
    nr = IntField()
    finished = BooleanField(default=False)

    task: ForeignKeyRelation[Task] = ForeignKeyField("rendering_server.Task")
