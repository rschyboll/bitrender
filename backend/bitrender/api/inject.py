from typing import Any, Callable

from antidote import world
from fastapi import BackgroundTasks, Depends


def InjectInRoute(
    inject_type: type,
    dependency: Callable[..., Any] | None = None,
    dependency_key: str | None = None,
) -> Callable[..., Any]:
    if dependency is None:

        def linker(background_tasks: BackgroundTasks) -> Any:
            inject_instance: Any = world.get(inject_type)
            instance_property_names = dir(inject_instance)
            if "background" in instance_property_names:
                setattr(inject_instance, "background", background_tasks)
            return inject_instance

        return linker

    def dependency_linker(
        background_tasks: BackgroundTasks,
        dependency_instance: Any = Depends(dependency),
    ) -> Any:
        inject_instance: Any = world.get(inject_type)
        instance_property_names = dir(inject_instance)
        if "background" in instance_property_names:
            setattr(inject_instance, "background", background_tasks)
        if dependency_key is not None:
            setattr(inject_instance, dependency_key, dependency_instance)
        return inject_instance

    return dependency_linker
