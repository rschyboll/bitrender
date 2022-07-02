from typing import Any, Callable

from antidote import world
from fastapi import Depends


def InjectInRoute(
    inject_type: type,
    dependency: Callable[..., Any] | None = None,
    dependency_key: str | None = None,
) -> Callable[..., Any]:
    if dependency is None:
        return lambda: world.get(inject_type)

    def dependency_linker(dependency_instance: Any = Depends(dependency)) -> Any:
        inject_instance: Any = world.get(inject_type)
        if dependency_key is not None:
            setattr(inject_instance, dependency_key, dependency_instance)
        return inject_instance

    return dependency_linker


class InjectInService:
    def __init__(self, dependency: Any, dependency_key: str) -> None:
        self.dependency = dependency
        self.dependency_key = dependency_key

    def __call__(self, inject_type: type) -> Any:
        inject_instance: Any = world.get(inject_type)
        setattr(inject_instance, self.dependency_key, self.dependency)
        return inject_instance
