"""Contains frontend router definition."""

from fastapi import APIRouter, Depends

from bitrender.api.deps.user import get_current_user
from bitrender.schemas import UserView
from bitrender.services.user import UserServices

frontend_router = APIRouter(prefix="/user")


@frontend_router.get("/me", dependencies=[Depends(get_current_user)])
async def get_me(services: UserServices = Depends()) -> UserView | None:
    return await services.user.get_current()
