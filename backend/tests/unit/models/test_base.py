"""Contains tests for BaseModel from bitrender.models.base."""
from tortoise.contrib.test import TruncationTestCase

from . import TestModel


class TestBaseModelData(TruncationTestCase):
    """TestCase containing tests for BaseModel with test data in the database."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_models: list[TestModel] = []

    async def asyncSetUp(self):
        """Creates database entries used in other tests"""
        for _ in range(0, 10):
            model = TestModel()
            await model.save()
            self.test_models.append(model)

    async def test_get_all(self):
        """Tests the get_all method with view set to False."""
        db_models = await TestModel.get_all()
        assert db_models == self.test_models

    async def test_get_all_view(self):
        """Tests the get_all method with view set to True."""
        views = [model.to_view() for model in self.test_models]
        db_views = await TestModel.get_all(True)
        assert views == db_views

    async def test_get_by_id(self):
        """Tests the get_by_id method with view set to False."""
        for model in self.test_models:
            db_model = await TestModel.get_by_id(model.id)
            assert model == db_model

    async def test_get_by_id_view(self):
        """Tests the get_by_id method with view set to True."""
        for model in self.test_models:
            view = model.to_view()
            db_view = await TestModel.get_by_id(model.id, True)
            assert view == db_view

    async def test_get_latest(self):
        """Tests the get_latest method with view set to False."""
        db_model = await TestModel.get_latest()
        assert db_model == self.test_models[len(self.test_models) - 1]

    async def test_get_latest_view(self):
        """Tests the get_latest method with view set to False."""
        db_view = await TestModel.get_latest(True)
        assert db_view == self.test_models[len(self.test_models) - 1].to_view()


class TestBaseModelNoData(TruncationTestCase):
    """TestCase containing tests for BaseModel without test data in the database."""

    async def test_get_latest_view_no_data(self):
        """Tests the get_latest method without data in the table."""
        db_model = await TestModel.get_latest(True)
        assert db_model is None
