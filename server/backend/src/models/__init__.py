from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model


class BaseModel(Model):
    id = UUIDField(pk=True)
    create_date = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
