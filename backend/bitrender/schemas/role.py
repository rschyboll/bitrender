"""This module contains the base class for all pydantic schemas."""
from datetime import datetime
from uuid import UUID

from bitrender.schemas import BaseView


class RoleView(BaseView):
    """s.

    Attributes:
        id (UUID): Primary key of the database entry.
        created_at (datetime): Datetime, when the entry was created.
        modified_at (datetime): Datetime, when the entry was last modified."""

    id: UUID
    created_at: datetime
    modified_at: datetime
