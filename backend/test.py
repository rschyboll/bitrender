from typing import Any, List


class TestClass:
    def __new__(cls, actions: int) -> Any:
        return cls(actions)


TestClass()
