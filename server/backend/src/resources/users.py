from fastapi import APIRouter

from schema.user import UserView
from storage import users as UserStorage

user_resources = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_resources.get('/')
async def get_user():
    return "Test"

@user_resources.get('/{login}')
async def get_user_by_login(login: str):
    return await UserStorage.get_by_login(login)

@user_resources.get('/id/{user_id}', response_model=UserView)
async def get_user_by_id(user_id: int):
    return await UserStorage.get(user_id)

@user_resources.get('s')
async def get_users():
    return []
