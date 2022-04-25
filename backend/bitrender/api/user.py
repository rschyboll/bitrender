"""TODO generate docstring"""
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from bitrender.auth.acl import AclAction
from bitrender.auth.deps import AuthCheck
from bitrender.models import User
from bitrender.schemas.user import UserCreate, UserSchema
from bitrender.services import user as UserService

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def get_me():
    """TODO generate docstring"""


@router.patch("/me", response_model=UserSchema)
async def update_me():
    """TODO generate docstring"""


@router.post("/create", response_model=UserSchema)
async def create_user(
    user_data: UserCreate = Body(...), role_id: UUID = Body(...), auth_check: AuthCheck = Depends()
):
    return await auth_check(UserService.create, AclAction.CREATE, (user_data, role_id))


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: UUID, auth_check: AuthCheck = Depends()):
    return await auth_check(User.get_by_id, AclAction.VIEW, (user_id,))


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: UUID):
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    pass
