from tortoise.models import Model
from tortoise.fields import UUIDField


class BaseModel(Model):
    id = UUIDField(pk=True)

    class Meta:
        abstract = True
