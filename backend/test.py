from typing import List, get

from antidote import implements, inject, interface


@interface
class ITestClass:
    def static(self, actions: str | List[str]) -> bool | None:
        pass


@implements(ITestClass).by_default
class TestClass(ITestClass):
    def static(self, actions: str | List[str]) -> bool | None:
        pass


def test(aclHelper: ITestClass = inject.me()):
    print(ITestClass)


test()
