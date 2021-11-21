from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CompositeAssignmentView(BaseModel):
    id: UUID
    create_date: datetime
    composite_task_id: UUID
    worker_id: UUID


class CompositeAssignmentCreate(BaseModel):
    composite_task_id: UUID
    worker_id: UUID
