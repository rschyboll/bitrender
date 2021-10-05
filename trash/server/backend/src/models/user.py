"""Module containing user ORM model"""
from models import BaseModel
from tortoise.fields.data import BinaryField, CharField, DatetimeField


class User(BaseModel):
    """User Model"""
    login = CharField(max_length = 32)
    password_hash = BinaryField()
    email = CharField(max_length = 64)
    register_date = DatetimeField()

    def __str__(self):
        return "id: {}\nlogin: {}\nemail: {}".format(self.id, self.login, self.email)

    class Meta:
        """Model metadata"""
        table="users"
