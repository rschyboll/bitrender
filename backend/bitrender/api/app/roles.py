"""Contains users router definition and its routes."""

from fastapi import APIRouter

from bitrender.api.inject import InjectInRoute

roles_router = APIRouter(prefix="/roles")


@roles_router.get("")
async def get_list() -> None:
    """"""
