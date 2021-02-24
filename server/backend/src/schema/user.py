"""Module containing schemas for user data"""
from pydantic import BaseModel

class User(BaseModel):
    """Base user schema"""
    login: str

class UserLogin(User):
    """Schema used in user loggin in"""
    password: str

class UserCreate(User):
    """Schema used in user creation"""
    email: str
    password: str

class UserView(User):
    """Schema used when asking for user data"""
    id: int
    email: str
