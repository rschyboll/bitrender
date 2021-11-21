from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubtaskAssignmentView(BaseModel):
    id: UUID
    create_date: datetime
    subtask_id: UUID
    worker_id: UUID


class SubtaskAssignmentCreate(BaseModel):
    subtask_id: UUID
    worker_id: UUID
