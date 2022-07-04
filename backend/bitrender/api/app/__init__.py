"""Contains app router definition."""
from fastapi import APIRouter

from .user import user_router

app_router = APIRouter(prefix="/app")
app_router.include_router(user_router)
