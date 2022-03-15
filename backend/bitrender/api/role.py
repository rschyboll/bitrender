from fastapi import APIRouter
from tortoise.transactions import atomic

from bitrender.schemas.user import RegisterData

router = APIRouter(prefix="/role")


@atomic()
@router.post("/create")
async def create(user_data: RegisterData):
    """TODO generate docstring"""
