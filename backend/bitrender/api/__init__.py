"""Contains api router definition."""
from fastapi import APIRouter

from bitrender.api.user import user_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router)
