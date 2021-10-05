from pydantic import BaseModel


class User(BaseModel):
    login: str

class UserCreate(User):
    email: str
    password: str

class UserView(User):
    id: int
    email: str

    class Config:
        orm_mode = True

class UserLogin(User):
    password: str
