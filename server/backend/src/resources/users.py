from fastapi import APIRouter

user_resources = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_resources.get('/')
async def get_user():
    return "Test"

@user_resources.get('/{login}')
async def get_user_by_login(login: str):
    return "Test2"

@user_resources.get('/id/{id}')
async def get_user_by_id(id: int):
    return "Test3"

@user_resources.get('s')
async def get_users():
    return []
