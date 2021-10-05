from controllers import login as LoginController
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from schema.user import UserView
from services import oauth2_scheme
from storage import users as UserStorage

user_resources = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_resources.get('/')
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await LoginController.get_current_user(token)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Could not validate credentials")

@user_resources.get('/{login}', response_model=UserView)
async def get_user_by_login(login: str):
    return await UserStorage.get_by_login(login)

@user_resources.get('/id/{user_id}', response_model=UserView)
async def get_user_by_id(user_id: int):
    return await UserStorage.get(user_id)

@user_resources.get('s')
async def get_users():
    return []
