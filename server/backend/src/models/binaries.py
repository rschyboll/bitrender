from tortoise.fields.data import TextField

from models import BaseModel


class Binary(BaseModel):
    version = TextField()
    url = TextField()
