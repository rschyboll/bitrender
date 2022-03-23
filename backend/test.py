"""This module contains dependencies for user authorization."""
import asyncio
import functools
from typing import Callable, Container, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class Test:
    @classmethod
    def __static_acl__(cls):
        return ["test2"]

    async def __dynamic_acl__(self):
        return ["test"]


def testt():
    def my_decorator(func: Callable[..., Test]) -> Callable:
        return_annotation = func.__annotations__["return"]

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if hasattr(return_annotation, "__static_acl__"):
                static_acl = return_annotation.__static_acl__()
                print(static_acl)

            return_object = await func(*args, **kwargs)
            if hasattr(return_object, "__dynamic_acl__"):
                dynamic_acl = await return_object.__dynamic_acl__()
                print(dynamic_acl)
            return return_object

        return wrapper

    return my_decorator


@testt()
async def test(i: int, s: str) -> Test:
    return Test()


asyncio.run(test(1, "2"))
