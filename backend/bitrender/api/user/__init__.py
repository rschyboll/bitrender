"""Contains frontend router definition."""
from typing import Any, Callable, Type, TypeVar
from uuid import UUID

from antidote import inject, injectable, world
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from bitrender.api.deps.user import get_current_user
from bitrender.api.user.responses import error_codes, user_by_id_responses, user_me_responses
from bitrender.errors.user import UserNotVerified
from bitrender.schemas import UserView
from bitrender.services.user import UserServices
from bitrender.services.user.interfaces.auth import IAuthService

user_router = APIRouter(prefix="/user")


@user_router.get(
    "/me",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_me_responses,
)
async def get_me(services: UserServices = Depends()) -> UserView:
    return await services.user.get_current()


@user_router.get("/test")
async def teset(test: IAuthService = Depends(Test(IAuthService))) -> None:
    print(test)


@user_router.post("/login")
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    services: UserServices = Depends(),
):
    token = await services.user.authenticate(credentials.username, credentials.password)
    response.set_cookie("access_token", f"Bearer {token}", httponly=True)


@user_router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_by_id_responses,
)
async def get_by_id(user_id: UUID, services: UserServices = Depends()) -> UserView:
    return await services.user.get_by_id(user_id)
