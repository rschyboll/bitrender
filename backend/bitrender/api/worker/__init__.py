"""Contains worker router definition."""
from fastapi import APIRouter

from bitrender.api.worker.v1 import v1_router

worker_router = APIRouter(prefix="/worker", tags=["worker"])

worker_router.include_router(v1_router)
