from uuid import UUID

from .base import BaseCreate, BaseView


class SubtaskAssignView(BaseView):
    subtask_id: UUID
    worker_id: UUID


class SubtaskAssignCreate(BaseCreate):
    subtask_id: UUID
    worker_id: UUID
