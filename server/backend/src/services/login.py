"""Module containing services for users"""
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from controllers import login as loginController
from schema.user import UserCreate, UserLogin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

user_services = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_services.post('/register')
async def register(user: UserCreate):
    """Endpoint used for creating/registering an user"""
    await loginController.register(user)

@user_services.post('/login')
async def login(user: UserLogin):
    """Endpoint used for logging in"""

@user_services.post('/logout')
async def logout():
    """Endpoint used for logging out"""
