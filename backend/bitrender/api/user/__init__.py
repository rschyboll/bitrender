"""Contains frontend router definition."""

from fastapi import APIRouter, Depends, HTTPException, status

from bitrender.api.deps.user import get_current_user
from bitrender.errors.auth import UnauthenticatedError
from bitrender.schemas import UserView
from bitrender.services.user import UserServices

frontend_router = APIRouter(prefix="/user")


@frontend_router.get("/me", dependencies=[Depends(get_current_user)])
async def get_me(services: UserServices = Depends()) -> UserView | None:
    try:
        return await services.user.get_current()
    except UnauthenticatedError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthenticatedError.code,
        ) from error
