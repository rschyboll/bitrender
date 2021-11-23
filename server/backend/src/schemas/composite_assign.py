from uuid import UUID

from .base import BaseCreate, BaseView


class CompositeAssignView(BaseView):
    composite_task_id: UUID
    worker_id: UUID


class CompositeAssignCreate(BaseCreate):
    composite_task_id: UUID
    worker_id: UUID
