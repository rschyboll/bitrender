"""TODO generate docstring"""

from http.client import HTTPException
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from bitrender.auth.deps import get_current_user_or_none
from bitrender.models import User
from bitrender.schemas.user import UserCreate, UserSchema
from bitrender.services import Services

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user_or_none)):
    """TODO generate docstring"""
    if current_user is None:
        raise HTTPException()
    return current_user


@router.post("/create", response_model=UserSchema)
async def create_user(
    user_data: UserCreate = Body(...),
    role_id: UUID = Body(...),
    services: Services = Depends(),
) -> User:
    return await services.user.create(user_data, role_id)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: UUID, services: Services = Depends()) -> User:
    return await services.auth.query(User.get_by_id(user_id))


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: UUID):
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    pass
