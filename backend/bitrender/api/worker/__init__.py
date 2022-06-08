"""Contains worker router definition."""
from fastapi import APIRouter

worker_router = APIRouter(prefix="/worker", tags=["worker"])
