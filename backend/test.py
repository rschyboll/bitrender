from typing import Generic, List, Literal, TypeVar

import uvicorn
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class InputModelInside(BaseModel):
    value2: int


class InputModel(BaseModel):
    value: List[int] | None = Query(None)


app = FastAPI()


@app.get("/get")
def get_data(input: InputModel = Query()) -> None:
    pass


uvicorn.run(app, host="0.0.0.0", port=8000)
