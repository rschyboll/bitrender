"""This module contains models used in unit testing."""
from bitrender.models.base import BaseModel
from bitrender.schemas.base import BaseView


class TestModel(BaseModel[BaseView]):
    # TODO zmiana nazwy na nie konfliktującą z nazwami testów
    """Database model used only for testing methods from BaseModel."""

    def to_view(self) -> BaseView:
        """Converts the testmodel to BaseView schema for testing purposes."""
        return BaseView.from_orm(self)
