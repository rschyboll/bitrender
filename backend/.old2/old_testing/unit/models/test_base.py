"""Contains tests for BaseModel model from bitrender.models.base."""
from __future__ import annotations

import json

from tortoise.contrib.test import TruncationTestCase
from tortoise.fields import ReverseRelation

from bitrender.core.acl import EVERYONE, AclAction, AclList, AclPermit
from tests.utils import TransactionTest
from tests.utils.mocks import AwaitableMock
from tests.utils.models import ExampleModel


class TestBaseModel(TruncationTestCase):
    """TestCase containing tests for BaseModel model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_models: list[ExampleModel] = []

    async def asyncSetUp(self):
        """Creates database entries used in other tests"""
        await super().asyncSetUp()
        for _ in range(0, 10):
            model = ExampleModel()
            await model.save()
            self.test_models.append(model)

    async def test_get_all(self):
        """Tests the get_all method with lock set to False."""
        db_models = await ExampleModel.get_all(False)
        assert db_models == self.test_models

    async def test_get_all_lock(self):
        """Tests the get_all method with lock set to True."""
        transaction_test = TransactionTest(
            ExampleModel.get_all, (True, False), ExampleModel.get_all, (True, True)
        )
        locked_models, not_locked_models = await transaction_test()
        assert locked_models == self.test_models
        assert len(not_locked_models) == 0

    async def test_get_by_id(self):
        """Tests the get_by_id method with lock set to False."""
        for model in self.test_models:
            db_model = await ExampleModel.get_by_id(model.id, False)
            assert model == db_model

    async def test_get_by_id_lock(self):
        """Tests the get_by_id method with lock set to True."""
        for model in self.test_models:
            transaction_test = TransactionTest(
                ExampleModel.get_by_id,
                (model.id, True),
                ExampleModel.get_all,
                (True, True),
            )
            locked_model, not_locked_models = await transaction_test()
            assert locked_model == model
            assert len(not_locked_models) == len(self.test_models) - 1
            assert locked_model not in not_locked_models

    async def test_get_latest(self):
        """Tests the get_latest method with lock set to False."""
        db_model = await ExampleModel.get_latest(False)
        assert db_model == self.test_models[len(self.test_models) - 1]

    async def test_get_latest_lock(self):
        """Tests the get_latest method with lock set to True."""
        transaction_test = TransactionTest(
            ExampleModel.get_latest,
            (True,),
            ExampleModel.get_all,
            (True, True),
        )
        locked_model, not_locked_models = await transaction_test()
        assert locked_model == self.test_models[len(self.test_models) - 1]
        assert locked_model not in not_locked_models

    async def test_get_amount(self):
        """Tests the get_latest_amount method with lock set to False."""
        db_models = await ExampleModel.get_amount(5, 0, "-created_at", False)
        test_models = self.test_models[-5:]
        test_models.reverse()
        assert db_models == test_models

    async def test_get_amount_lock(self):
        """Tests the get_latest_amount method with lock set to True."""
        transaction_test = TransactionTest(
            ExampleModel.get_amount,
            (5, 0, "-created_at", True),
            ExampleModel.get_all,
            (True, True),
        )
        locked_models, not_locked_models = await transaction_test()
        test_models = self.test_models[-5:]
        test_models.reverse()
        assert locked_models == test_models
        for model in locked_models:
            assert model not in not_locked_models

    async def test_acl(self):
        """Tests the __dacl__ and __sacl__ methods."""
        assert len(await ExampleModel().__dacl__()) != 0
        assert len(ExampleModel.__sacl__()) != 0

    async def test_extend_dacl(self):
        """Tests the extend_dacl method."""
        reverse_relation_model_count = 10
        reverse_relation_models = [ExampleModel() for _ in range(0, reverse_relation_model_count)]
        model = ExampleModel()
        reverse_relation_dacl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        model_dacl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]

        def __generate__dacl__(dacl: list[AclList]):
            async def __dacl__() -> list[AclList]:
                return dacl

            return __dacl__

        for reverse_relation_model in reverse_relation_models:
            setattr(reverse_relation_model, "__dacl__", __generate__dacl__(reverse_relation_dacl))
        setattr(model, "__dacl__", __generate__dacl__(model_dacl))

        reverse_relation = ReverseRelation(ExampleModel, "", ExampleModel, "")
        reverse_relation._fetched = True  # pylint: disable=W0212
        reverse_relation.related_objects = reverse_relation_models
        tested_acl = [
            *model_dacl,
            *[reverse_relation_dacl[0] for i in range(0, reverse_relation_model_count)],
        ]
        test_acl: list[AclList] = []

        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(reverse_relation, test_acl)

        assert json.dumps(tested_acl) == json.dumps(test_acl)

    async def test_extend_dacl_not_awaited(self):
        """Tests the extend_dacl method with not awaited relations."""
        reverse_relation_model_count = 10
        reverse_relation_models = [ExampleModel() for _ in range(0, reverse_relation_model_count)]
        model = ExampleModel()
        reverse_relation_dacl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        model_dacl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        foreign_relation = AwaitableMock(return_value=model)

        def __generate__dacl__(dacl: list[AclList]):
            async def __dacl__() -> list[AclList]:
                return dacl

            return __dacl__

        for reverse_relation_model in reverse_relation_models:
            setattr(reverse_relation_model, "__dacl__", __generate__dacl__(reverse_relation_dacl))
        setattr(model, "__dacl__", __generate__dacl__(model_dacl))

        reverse_relation = ReverseRelation(ExampleModel, "", ExampleModel, "")
        reverse_relation.related_objects = reverse_relation_models
        test_acl: list[AclList] = []

        await ExampleModel.extend_dacl(foreign_relation, test_acl)
        await ExampleModel.extend_dacl(reverse_relation, test_acl)

        assert len(test_acl) == 0
