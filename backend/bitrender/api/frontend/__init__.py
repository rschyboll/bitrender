"""Contains frontend router definition."""
from fastapi import APIRouter

from bitrender.api.frontend.v1 import v1_router

frontend_router = APIRouter(prefix="/frontend", tags=["frontend"])

frontend_router.include_router(v1_router)
