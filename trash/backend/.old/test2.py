from typing import TypeVar, Type

_TypeT = TypeVar("_TypeT", bound="Test")


class TestMeta(type):
    def __getitem__(cls, key: int) -> int:
        pass


class Test(metaclass=TestMeta):
    def __class_getitem__(cls, key: int) -> int:
        pass


Test.__getitem__(2)
test = Test[4]
print(test)
