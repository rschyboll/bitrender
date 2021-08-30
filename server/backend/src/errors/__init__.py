from fastapi import FastAPI

from errors.storage import add_storage_exception_handlers


def add_exception_handlers(app: FastAPI) -> None:
    add_storage_exception_handlers(app)
