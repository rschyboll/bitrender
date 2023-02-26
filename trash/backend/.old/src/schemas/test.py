from typing import Optional
from uuid import UUID

from .base import BaseCreate, BaseView


class TestView(BaseView):
    sync_time: Optional[float]
    render_time: Optional[float]
    error: bool


class TestCreate(BaseCreate):
    worker_id: UUID
