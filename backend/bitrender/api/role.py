from uuid import UUID

from fastapi import APIRouter, Depends
from tortoise.transactions import atomic

from bitrender.base.auth import UserWithPermissions
from bitrender.models import Permission
from bitrender.schemas import RoleView

router = APIRouter(prefix="/role")


@router.get("/all")
async def get(name: str) -> RoleView:
    """TODO generate docstring"""


@router.get("/id/${}")
async def get_by_id(role_id: str) -> RoleView:
    """TODO generate docstring"""


@atomic()
@router.post("/create", dependencies=[Depends(UserWithPermissions(Permission.CREATE_ROLE))])
async def create(name: str) -> RoleView:
    """TODO generate docstring"""


@atomic()
@router.post("/update", dependencies=[Depends(UserWithPermissions(Permission.UPDATE_ROLE))])
async def update(role_id: UUID) -> RoleView:
    """TODO generate docstring"""


@atomic()
@router.post("/delete", dependencies=[Depends(UserWithPermissions(Permission.DELETE_ROLE))])
async def delete(role_id: UUID) -> RoleView:
    """TODO generate docstring"""
