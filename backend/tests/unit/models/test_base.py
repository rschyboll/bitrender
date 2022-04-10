"""Contains tests for BaseModel from bitrender.models.base."""
import asyncio
from typing import Any, Callable, Coroutine, TypeVar

from tortoise.contrib.test import TruncationTestCase
from tortoise.transactions import in_transaction

from . import ExampleModel

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")

Selector = Callable[..., Coroutine[Any, Any, T]]


class TransactionTest:
    """Helper class used for testing transactions.
    When calling it's instance, it launches two transactions in paralell.\n
    The first transaction is launched first, and it wait's for the second transaction to finish."""

    def __init__(self, select1: Selector[T1], args1: tuple, select2: Selector[T2], args2: tuple):
        """Creates an instance of the class.

        Args:
            select1 (Selector[T1]): First selector, that will keep it's transaction running,
                until the second selector finishes.
            args1 (tuple): Args that will be passed to the second selector.
            select2 (Selector[T2]): Second selector.
            args2 (tuple): Args that will be passed to the second selector"""
        self.__select1 = select1
        self.__select2 = select2
        self.__args1 = args1
        self.__args2 = args2
        self.__event_selected = asyncio.Event()
        self.__event = asyncio.Event()

    async def __call__(self) -> tuple[T1, T2]:
        """Calls the selectors in seperate transactions and returns their selected values.

        Returns:
            tuple[T1, T2]: Values of the selectors."""
        task1 = asyncio.create_task(self.__in_transaction(self.__select1, True, *self.__args1))
        task2 = asyncio.create_task(self.__in_transaction(self.__select2, False, *self.__args2))
        return (await task1, await task2)

    async def __in_transaction(self, select: Selector[T], wait: bool, *args) -> T:
        async with in_transaction():
            if not wait:
                await self.__event_selected.wait()
            entries = await select(*args)
            if wait:
                self.__event_selected.set()
                await self.__event.wait()
            else:
                self.__event.set()
            return entries


class TestBaseModel(TruncationTestCase):
    """TestCase containing tests for BaseModel with test data in the database."""

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
        assert await ExampleModel().__dacl__() is None
        assert ExampleModel.__sacl__() is None
