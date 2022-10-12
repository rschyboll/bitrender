"""Contains tests for BaseModel model from bitrender.models.base."""
from __future__ import annotations

from typing import Any, Callable, Coroutine, cast

from tortoise.contrib.test import TruncationTestCase
from tortoise.fields import ForeignKeyRelation, ReverseRelation

from bitrender.core.acl import EVERYONE, AclAction, AclList, AclPermit
from bitrender.enums.list_request import SearchRule, SortOrder
from bitrender.schemas import ListRequestInput, ListRequestPage, ListRequestSearch, ListRequestSort
from tests.utils.generators import generate_example_models
from tests.utils.models import ExampleModel
from tests.utils.transactions import TransactionTest


class TestBaseModel(TruncationTestCase):
    """Test case for testing the BaseModel model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.test_models: list[ExampleModel] = []

    async def asyncSetUp(self) -> None:
        """Creates database entries used in other tests."""
        await super().asyncSetUp()
        self.test_models = await generate_example_models(10)

    async def test_get_all(self) -> None:
        """Tests the get_all method with the lock parameter set to False."""
        db_models = await ExampleModel.get_all(False)
        assert db_models == self.test_models

    async def test_get_all_lock(self) -> None:
        """Tests the get_all method with the lock parameter set to True."""
        transaction_test = TransactionTest(
            ExampleModel.get_all, (True, False), ExampleModel.get_all, (True, True)
        )
        locked_models, not_locked_models = await transaction_test()
        assert locked_models == self.test_models
        assert len(not_locked_models) == 0

    async def test_get_by_id(self) -> None:
        """Tests the get_by_id method with the lock parameter set to False."""
        for model in self.test_models:
            db_model = await ExampleModel.get_by_id(model.id, False)
            assert model == db_model

    async def test_get_by_id_lock(self) -> None:
        """Tests the get_by_id method with the lock parameter set to True."""
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

    async def test_get_latest(self) -> None:
        """Tests the get_latest method with the lock parameter set to False."""
        db_model = await ExampleModel.get_latest(False)
        assert db_model == self.test_models[len(self.test_models) - 1]

    async def test_get_latest_lock(self) -> None:
        """Tests the get_latest method with the lock parameter set to True."""
        transaction_test = TransactionTest(
            ExampleModel.get_latest,
            (True,),
            ExampleModel.get_all,
            (True, True),
        )
        locked_model, not_locked_models = await transaction_test()
        assert locked_model == self.test_models[len(self.test_models) - 1]
        assert locked_model not in not_locked_models

    async def test_get_amount(self) -> None:
        """Tests the get_amount method with the lock parameter set to False."""
        db_models = await ExampleModel.get_amount(5, 0, "-created_at", False)
        test_models = self.test_models[-5:]
        test_models.reverse()
        assert db_models == test_models

    async def test_get_amount_lock(self) -> None:
        """Tests the get_amount method with the lock parameter set to True."""
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

    async def test_get_list(self) -> None:
        """Tests the get_list method with the lock parameter set to False"""
        request_input = ListRequestInput[ExampleModel.columns](
            sort=ListRequestSort(column="created_at", order=SortOrder.ASC),
            page=ListRequestPage(records_per_page=5, page_nr=0),
            search=[
                ListRequestSearch(
                    column="id", rule=SearchRule.NOTEQUAL, value=self.test_models[0].id
                )
            ],
        )
        db_models = await ExampleModel.get_list(request_input, False)
        assert db_models == self.test_models[1:6]

    async def test_get_list_lock(self) -> None:
        """Tests the get_list method with the lock parameter set to True"""
        request_input = ListRequestInput[ExampleModel.columns](
            sort=ListRequestSort(column="created_at", order=SortOrder.ASC),
            page=ListRequestPage(records_per_page=5, page_nr=0),
            search=[
                ListRequestSearch(
                    column="id", rule=SearchRule.NOTEQUAL, value=self.test_models[0].id
                )
            ],
        )
        transaction_test = TransactionTest(
            ExampleModel.get_list,
            (request_input, True),
            ExampleModel.get_all,
            (True, True),
        )
        locked_models, not_locked_models = await transaction_test()
        for model in self.test_models:
            assert model in [*not_locked_models, *locked_models]
        assert len([*not_locked_models, *locked_models]) == len(self.test_models)
        assert locked_models == self.test_models[1:6]

    async def test_get_list_sort(self) -> None:
        """Tests the get_list method with only the sort parameter"""
        request_input_asc = ListRequestInput[ExampleModel.columns](
            sort=ListRequestSort(column="created_at", order=SortOrder.ASC),
        )
        request_input_desc = ListRequestInput[ExampleModel.columns](
            sort=ListRequestSort(column="created_at", order=SortOrder.DESC),
        )
        request_input_default = ListRequestInput[ExampleModel.columns]()
        db_models_asc = await ExampleModel.get_list(request_input_asc)
        db_models_desc = await ExampleModel.get_list(request_input_desc)
        db_models_default = await ExampleModel.get_list(request_input_default)
        assert db_models_asc == self.test_models
        assert db_models_desc == self.test_models[::-1]
        assert db_models_default == self.test_models[::-1]

    async def test_get_list_search(self) -> None:
        """Tests the get_list method with only the search parameter"""
        request_input_equal = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(column="id", rule=SearchRule.EQUAL, value=self.test_models[0].id)
            ]
        )
        request_input_not_equal = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="id", rule=SearchRule.NOTEQUAL, value=self.test_models[0].id
                )
            ]
        )
        request_input_begins_with = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="char_field",
                    rule=SearchRule.BEGINSWITH,
                    value=self.test_models[0].char_field[
                        0 : int(len(self.test_models[0].char_field) / 2)
                    ],
                )
            ]
        )
        request_input_greater = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="int_field",
                    rule=SearchRule.GREATER,
                    value=self.test_models[int(len(self.test_models) / 2)].int_field,
                )
            ]
        )
        request_input_greater_or_equal = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="int_field",
                    rule=SearchRule.GREATEROREQUAL,
                    value=self.test_models[int(len(self.test_models) / 2)].int_field,
                )
            ]
        )
        request_input_less = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="int_field",
                    rule=SearchRule.LESS,
                    value=self.test_models[int(len(self.test_models) / 2)].int_field,
                )
            ]
        )
        request_input_less_or_equal = ListRequestInput[ExampleModel.columns](
            search=[
                ListRequestSearch(
                    column="int_field",
                    rule=SearchRule.LESSOREQUAL,
                    value=self.test_models[int(len(self.test_models) / 2)].int_field,
                )
            ]
        )
        db_models_equal = await ExampleModel.get_list(request_input_equal)
        db_models_not_equal = await ExampleModel.get_list(request_input_not_equal)
        db_models_begins_with = await ExampleModel.get_list(request_input_begins_with)
        db_models_greater = await ExampleModel.get_list(request_input_greater)
        db_models_greater_or_equal = await ExampleModel.get_list(request_input_greater_or_equal)
        db_models_less = await ExampleModel.get_list(request_input_less)
        db_models_less_or_equal = await ExampleModel.get_list(request_input_less_or_equal)
        assert db_models_equal == [self.test_models[0]]
        assert db_models_not_equal == self.test_models[:0:-1]
        assert db_models_begins_with == [self.test_models[0]]
        assert (
            db_models_greater
            == self.test_models[len(self.test_models) : int(len(self.test_models) / 2) : -1]
        )
        assert (
            db_models_greater_or_equal
            == self.test_models[len(self.test_models) : int(len(self.test_models) / 2) - 1 : -1]
        )
        assert db_models_less == self.test_models[int(len(self.test_models) / 2) - 1 :: -1]
        assert db_models_less_or_equal == self.test_models[int(len(self.test_models) / 2) :: -1]

    async def test_get_list_page(self) -> None:
        """Tests the get_list method with only the search parameter"""
        request_input_page_1 = ListRequestInput[ExampleModel.columns](
            page=ListRequestPage(records_per_page=5, page_nr=0)
        )
        request_input_page_2 = ListRequestInput[ExampleModel.columns](
            page=ListRequestPage(records_per_page=5, page_nr=1)
        )
        db_models_page_1 = await ExampleModel.get_list(request_input_page_1)
        db_models_page_2 = await ExampleModel.get_list(request_input_page_2)
        assert db_models_page_1 == self.test_models[9:4:-1]
        assert db_models_page_2 == self.test_models[4::-1]

    async def test_acl(self) -> None:
        """Tests the __dacl__ and __sacl__ methods."""
        assert len(await ExampleModel().__dacl__()) != 0
        assert len(ExampleModel.__sacl__()) != 0

    async def test_extend_dacl_foreign_relation(self) -> None:
        """Tests the extends_dacl method with a fetched foreign_relation passed as parameter."""
        model_acl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        relation_acl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        model = self.__prepare_model_with_dacl(model_acl)
        relation = self.__prepare_model_with_dacl(relation_acl)
        test_acl: list[AclList] = []
        expected_acl = [*model_acl, *relation_acl]
        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(relation, test_acl)

        assert expected_acl == test_acl

    async def test_extend_dacl_foreing_relation_not_fetched(self) -> None:
        """Tests the extends_dacl method with a not fetched foreign_relation passed as parameter."""
        model_acl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        relation_acl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        model = self.__prepare_model_with_dacl(model_acl)
        relation = self.__create_foreign_relation(self.__prepare_model_with_dacl(relation_acl))
        test_acl: list[AclList] = []
        expected_acl = [*model_acl]
        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(relation, test_acl)

        assert expected_acl == test_acl

    async def test_extend_dacl_reverse_relation(self) -> None:
        """Tests the extends_dacl method with a fetched reverse_relation passed as parameter."""
        model_acl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        relation_acl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        model = self.__prepare_model_with_dacl(model_acl)
        relation = self.__prepare_reverse_relation_with_dacl(relation_acl, 10, True)
        test_acl: list[AclList] = []
        expected_acl = [
            *model_acl,
            *[relation_acl[0] for i in range(0, 10)],
        ]
        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(relation, test_acl)

        assert expected_acl == test_acl

    async def test_extend_dacl_reverse_relation_not_fetched(self) -> None:
        """Tests the extends_dacl method with a fetched reverse_relation passed as parameter."""
        model_acl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        relation_acl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        model = self.__prepare_model_with_dacl(model_acl)
        relation = self.__prepare_reverse_relation_with_dacl(relation_acl, 10, False)
        test_acl: list[AclList] = []
        expected_acl = [*model_acl]
        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(relation, test_acl)

        assert expected_acl == test_acl

    async def test_extend_dacl_reverse_relation_not_basemodel(self) -> None:
        """Tests the extends_dacl method with a fetched reverse_relation passed as parameter."""
        model_acl: list[AclList] = [[(AclPermit.DENY, EVERYONE, AclAction.VIEW)]]
        relation_acl: list[AclList] = [[(AclPermit.NOTALLOW, "user:test2", AclAction.EDIT)]]
        model = self.__prepare_model_with_dacl(model_acl)
        relation = self.__prepare_reverse_relation_with_dacl(relation_acl, 10, True)
        relation.related_objects = [1, 2, 3]  # type: ignore
        test_acl: list[AclList] = []
        expected_acl: list[AclList] = [*model_acl]
        await ExampleModel.extend_dacl(model, test_acl)
        await ExampleModel.extend_dacl(relation, test_acl)

        assert expected_acl == test_acl

    def __prepare_reverse_relation_with_dacl(
        self, relation_models_dacl: list[AclList], model_count: int, fetched: bool
    ) -> ReverseRelation[ExampleModel]:
        relation_models = [ExampleModel() for _ in range(0, model_count)]
        for model in relation_models:
            setattr(model, "__dacl__", self.__create_dacl_callback(relation_models_dacl))

        relation = ReverseRelation(ExampleModel, "", ExampleModel(), "")
        relation._fetched = fetched  # pylint: disable=W0212
        relation.related_objects = relation_models
        return relation

    def __prepare_model_with_dacl(self, model_dacl: list[AclList]) -> ExampleModel:
        model = ExampleModel()
        setattr(model, "__dacl__", self.__create_dacl_callback(model_dacl))
        return model

    def __create_dacl_callback(
        self, dacl: list[AclList]
    ) -> Callable[..., Coroutine[Any, Any, list[AclList]]]:
        async def __dacl__() -> list[AclList]:
            return dacl

        return __dacl__

    def __create_foreign_relation(self, model: ExampleModel) -> ForeignKeyRelation[ExampleModel]:
        async def __relation__() -> ExampleModel:
            return model

        return cast(ForeignKeyRelation[ExampleModel], __relation__)
