"""Module containing services for users"""
from fastapi import APIRouter
from controllers import users as userController
from schema.user import UserCreate, UserLogin

user_services = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_services.post('/register')
async def register(user: UserCreate):
    """Endpoint used for creating/registering an user"""
    userController.register(user)

@user_services.post('/login')
async def login(user: UserLogin):
    """Endpoint used for logging in"""

@user_services.post('/logout')
async def logout():
    """Endpoint used for logging out"""
