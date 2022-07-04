"""Contains api router definition."""
from fastapi import APIRouter

from bitrender.api.app import app_router

api_router = APIRouter(prefix="/api")

api_router.include_router(app_router)
