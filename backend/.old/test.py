# pylint: disable=unused-import
# pylint: disable=invalid-name
from datetime import datetime
import typing
import inspect
from typing import Generic

from typing import Generic, List, Literal, Type, TypeVar, Union, overload, Optional, Any
from uuid import UUID

from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model, ModelMeta
from tortoise.queryset import QuerySetSingle


class GenericMeta(type):
    def __class_getitem__() -> Any:
        print("TEST")


T = TypeVar("T")


class TestModel(Generic[T], metaclass=GenericMeta):
    pass


test = TestModel[int]


class Test(TestModel[int]):
    pass


print(inspect.getsource(TestModel.__class_getitem__))
