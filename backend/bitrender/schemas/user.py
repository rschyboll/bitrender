from pydantic import BaseModel as BaseSchema

from bitrender.schemas import BaseView


class RegisterData(BaseSchema):
    password: str
    email: str


class UserView(BaseView):
    username: str
    email: str
