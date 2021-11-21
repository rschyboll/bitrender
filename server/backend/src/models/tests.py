from __future__ import annotations

from tortoise.fields.data import BooleanField, FloatField
from tortoise.fields.relational import ReverseRelation

from models import BaseModel
from models.workers import Worker


class Test(BaseModel):
    sync_time = FloatField(null=True, default=None)
    render_time = FloatField(null=True, default=None)

    error = BooleanField(default=False)

    worker: ReverseRelation[Worker]
