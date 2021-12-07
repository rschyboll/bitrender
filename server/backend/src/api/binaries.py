from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from models import Binary
from schemas import BinaryCreate, BinaryView

router = APIRouter(prefix="/binaries")


@router.get("/")
async def get_binaries() -> List[BinaryView]:
    return await Binary.get_all(True)


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_task(binary: BinaryCreate) -> BinaryView:
    return (await Binary.make(**binary.dict())).to_view()


@router.get("/latest")
async def get_latest() -> BinaryView:
    binary = await Binary.get_latest(True)
    if binary is not None:
        return binary
    raise HTTPException(404)


@router.get("/{binary_id}")
async def get_task_by_id(binary_id: UUID) -> BinaryView:
    return await Binary.get_by_id(binary_id, True)


@router.delete("/delete")
async def delete(binary_id: UUID) -> None:
    await (await Binary.get_by_id(binary_id)).delete()
