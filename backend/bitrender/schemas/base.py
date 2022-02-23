"""This module contains the base class for all pydantic schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseView(BaseModel):
    """Class that serves as the base for all pydantic schemas.

    Attributes:
        id (UUID): Primary key of the database entry.
        create_time (datetime): Datetime, when the entry was created."""

    id: UUID
    create_date: datetime

    class Config:
        """BaseView config."""

        orm_mode = True
