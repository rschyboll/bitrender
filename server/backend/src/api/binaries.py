from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status

from schemas.binaries import BinaryCreate, BinaryView
from storage import binaries as BinaryStorage

router = APIRouter(prefix="/binaries")


@router.get("/")
async def get_binaries() -> List[BinaryView]:
    return await BinaryStorage.get()


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=BinaryView)
async def create_task(binary: BinaryCreate) -> BinaryView:
    return await BinaryStorage.create(binary)


@router.get("/{binary_id}", response_model=BinaryView)
async def get_task_by_id(binary_id: UUID) -> Optional[BinaryView]:
    return await BinaryStorage.get_by_id(binary_id)


@router.get("/latest", response_model=BinaryView)
async def get_latest() -> BinaryView:
    return await BinaryStorage.get_latest()
