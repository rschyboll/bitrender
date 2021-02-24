"""Module containing user ORM model"""
from tortoise.models import Model
from tortoise.fields.data import BinaryField, CharField, DatetimeField, UUIDField

class User(Model):
    """User ORM Model"""
    id = UUIDField(pk = True)
    login = CharField(max_length = 32)
    password_hash = BinaryField()
    email = CharField(max_length = 64)
    register_date = DatetimeField()

    def __str__(self):
        return "id: {}\nlogin: {}\nemail: {}".format(self.id, self.login, self.email)
