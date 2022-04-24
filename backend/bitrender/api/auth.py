"""TODO generate docstring"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from bitrender.schemas.user import UserCreate, UserSchema
from bitrender.services import user as UserService

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate):
    return await UserService.register(data)


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    pass


@router.post("/logout")
async def logout():
    pass


@router.post("/request-verify-token")
async def request_verify_token(email: EmailStr):
    pass


@router.post("/verify")
async def verify(token: str):
    pass


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    pass


@router.post("/reset-password")
async def reset_password(token: str, password: str):
    pass
