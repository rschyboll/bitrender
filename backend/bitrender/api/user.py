"""TODO generate docstring"""
from uuid import UUID

from fastapi import APIRouter

from bitrender.schemas.user import UserSchema

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def get_me():
    """TODO generate docstring"""


@router.patch("/me", response_model=UserSchema)
async def update_me():
    """TODO generate docstring"""


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: UUID):
    pass


@router.post("/{user_id}")
async def create_user():
    pass


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(user_id: UUID):
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    pass
