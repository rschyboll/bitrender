"""Contains utilities for helping with query parameters in request."""
from typing import Any

from fastapi import Depends, HTTPException, Query
from pydantic import ValidationError, parse_obj_as
from pydantic.types import Json


def json_param(param_name: str, model: Any, **query_kwargs: Any) -> Any:
    """Parse JSON-encoded query parameters as pydantic models.
    The function returns a `Depends()` instance that takes the JSON-encoded value from
    the query parameter `param_name` and converts it to a Pydantic model, defined
    by the `model` attribute."""

    def get_parsed_object(value: Json = Query(alias=param_name, **query_kwargs)) -> Any:
        try:
            return parse_obj_as(model, value)
        except ValidationError as err:
            raise HTTPException(400, detail=err.errors()) from err

    return Depends(get_parsed_object)
