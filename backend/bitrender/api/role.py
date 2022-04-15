"""TODO generate docstring"""
from fastapi import APIRouter, Depends

from bitrender.base.acl import AclAction
from bitrender.base.auth import AuthCheck
from bitrender.models.role import Role
from bitrender.schemas.role import RoleCreateData, RoleSchema

router = APIRouter(prefix="/role")


async def __create_role(data: RoleCreateData) -> Role:
    pass


@router.post("/create", response_model=RoleSchema)
async def create(data: RoleCreateData, auth_check: AuthCheck = Depends(AuthCheck)) -> Role:
    """TODO generate docstring"""
    role = await auth_check(__create_role, AclAction.CREATE, [], (data,))
    return role
