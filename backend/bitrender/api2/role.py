"""TODO generate docstring"""


from fastapi import APIRouter

from bitrender.models import Role
from bitrender.schemas.role import RoleCreate, RoleSchema

router = APIRouter(prefix="/role", tags=["role"])


@router.post("/create", response_model=RoleSchema)
async def create(data: RoleCreate):
    return await Role.create(**data.dict())
