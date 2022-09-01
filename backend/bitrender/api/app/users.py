"""Contains users router definition and its routes."""

from fastapi import APIRouter

from bitrender.api.inject import InjectInRoute

users_router = APIRouter(prefix="/users")
