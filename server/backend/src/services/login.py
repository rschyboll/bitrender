from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers import login as LoginController
from schema.user import UserCreate, UserLogin

user_services = APIRouter(
    prefix='/user',
    tags=['users']
)

@user_services.post('/register')
async def register(user: UserCreate):
    await LoginController.register(user)

@user_services.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserLogin(login=form_data.username, password=form_data.password)
    token = await LoginController.login(user)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": token, "token_type": "bearer"}

@user_services.post('/logout')
async def logout():
    pass
