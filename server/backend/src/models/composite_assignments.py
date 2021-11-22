from typing import TYPE_CHECKING

from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from models import BaseModel

if TYPE_CHECKING:
    from models.composite_tasks import CompositeTask
    from models.workers import Worker
else:
    Worker = object
    CompositeTask = object


class CompositeAssignment(BaseModel):
    composite_task: ForeignKeyRelation[CompositeTask] = ForeignKeyField(
        "rendering_server.CompositeTask"
    )
    worker: ForeignKeyRelation[Worker] = ForeignKeyField("rendering_server.Worker")
