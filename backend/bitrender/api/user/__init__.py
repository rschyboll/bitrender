"""Contains frontend router definition."""
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from bitrender.api.deps.user import UserContext, get_current_user
from bitrender.api.user.responses import user_by_id_responses, user_me_responses
from bitrender.schemas import UserView
from bitrender.services.inject import InjectInRoute
from bitrender.services.user import IUserService

user_router = APIRouter(prefix="/user")


@user_router.post("/login")
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> None:
    token = await user_service.authenticate(credentials.username, credentials.password)
    response.set_cookie("access_token", f"Bearer {token}", httponly=True)


@user_router.post("/register")
async def register(
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context"))
) -> None:
    print(user_service)


@user_router.get(
    "/me",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_me_responses,
)
async def get_me(
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    return await user_service.get_current()


@user_router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_by_id_responses,
)
async def get_by_id(
    user_id: UUID,
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    return await user_service.get_by_id(user_id)
