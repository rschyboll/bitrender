"""Contains the base class for all pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as Schema


class BaseSchema(Schema):
    """Class that serves as the base for all pydantic schemas.

    Attributes:
        id (UUID): Primary key of the database entry.
        created_at (datetime): Datetime, when the entry was created.
        modified_at (datetime): Datetime, when the entry was modified."""

    id: UUID
    created_at: datetime
    modified_at: datetime

    class Config:
        """BaseSchema config."""
        orm_mode = True
