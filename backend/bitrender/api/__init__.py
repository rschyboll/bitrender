"""Contains api router definition."""
from fastapi import APIRouter

from bitrender.api.user import frontend_router
from bitrender.api.worker import worker_router

api_router = APIRouter(prefix="/api")

api_router.include_router(worker_router)
api_router.include_router(frontend_router)
