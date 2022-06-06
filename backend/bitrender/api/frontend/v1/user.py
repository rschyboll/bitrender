"""Contains frontend router definition."""
from fastapi import APIRouter

from bitrender.schemas import UserView

user_router = APIRouter(prefix="/user")


@user_router.get("/me", response_model=UserView)
async def get_me():
    """Returns current users data."""
