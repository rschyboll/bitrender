from uuid import UUID
from datetime import datetime
from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model


class BaseModel(Model):
    id: UUID = UUIDField(pk=True)
    create_date: datetime = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
