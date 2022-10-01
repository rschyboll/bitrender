"""Contains helpers easier for injecting into services with antidote."""
from typing import Any

from antidote import world


class InjectInService:
    """Class that is used for injecting some instance with antidote,\
         but with some additional outside context.

    When creating an instance of the class, \
        it is passed a additional dependency to pass to the injected instance.

    It takes the dependency, and uses setattr to pass the dependency to the injected instance."""

    def __init__(self, context: Any, context_key: str) -> None:
        self.context = context
        self.context_key = context_key

    def __call__(self, dependency_type: type) -> Any:
        dependency: Any = world.get(dependency_type)
        setattr(dependency, self.context_key, self.context)
        return dependency
