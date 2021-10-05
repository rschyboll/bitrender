from tortoise.fields import UUIDField
from tortoise.models import Model


class BaseModel(Model):
    id = UUIDField(pk=True)

    class Meta:
        abstract = True
