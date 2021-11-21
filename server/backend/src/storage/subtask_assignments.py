from typing import List
from uuid import UUID

from models.subtasks_assignments import SubtaskAssignment
from schemas.subtask_assignments import SubtaskAssignmentCreate, SubtaskAssignmentView


async def create(subtask_assignment: SubtaskAssignmentCreate) -> SubtaskAssignmentView:
    subtask_assignment_db = SubtaskAssignment(**subtask_assignment.dict())
    await subtask_assignment_db.save()
    return SubtaskAssignmentView.from_orm(subtask_assignment_db)


async def get() -> List[SubtaskAssignmentView]:
    subtask_assignments = await SubtaskAssignment.all()
    subtask_assignment_views: List[SubtaskAssignmentView] = []
    for subtask_assignment in subtask_assignments:
        subtask_assignment_views.append(
            SubtaskAssignmentView.from_orm(subtask_assignment)
        )
    return subtask_assignment_views


async def get_failed_assignments(
    worker_id: UUID, subtask_id: UUID
) -> List[SubtaskAssignmentView]:
    subtask_assignment = (
        await SubtaskAssignment.filter(worker_id=worker_id, subtask_id=subtask_id)
        .select_related("subtask")
        .select_for_update()
    )

    subtask_assignments = await SubtaskAssignment.filter(
        worker_id=worker_id, subtask__error=True, subtask__frame__task__id=task_id
    )
    subtask_assignment_views: List[SubtaskAssignmentView] = []
    for subtask_assignment in subtask_assignments:
        subtask_assignment_views.append(
            SubtaskAssignmentView.from_orm(subtask_assignment)
        )
    return subtask_assignment_views
