from typing import Any

from antidote import world


class InjectInService:
    def __init__(self, dependency: Any, dependency_key: str) -> None:
        self.dependency = dependency
        self.dependency_key = dependency_key

    def __call__(self, inject_type: type) -> Any:
        inject_instance: Any = world.get(inject_type)
        setattr(inject_instance, self.dependency_key, self.dependency)
        return inject_instance
