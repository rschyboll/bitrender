from typing import List, Optional, get_origin, Union, get_args, get_type_hints
import inspect


def is_optional(field) -> bool:
    return get_origin(field) is Union and type(None) in get_args(field)


def my_function(test: int) -> Optional[int]:
    pass


signature = inspect.signature(my_function)
print(signature)
print(get_origin(signature.return_annotation))
print(signature.return_annotation == Optional[int])  # False
print(get_type_hints(my_function))
