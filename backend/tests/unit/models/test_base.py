import pytest
from tortoise.contrib.test import TruncationTestCase

from bitrender.models import BaseModel
from bitrender.schemas import BaseView


class TestModel(BaseModel[BaseView]):
    """Model used only for testing methods from BaseModel class."""

    def to_view(self) -> BaseView:
        """Converts the model to it's corresponding pydantic schema."""
        return BaseView.from_orm(self)


class TestSomething(TruncationTestCase):
    async def test_something(self):
        assert 2 == 4
