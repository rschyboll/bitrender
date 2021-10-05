from fastapi import FastAPI

from errors.storage import add_storage_exception_handlers


class ServerException(Exception):
    """Base server exception"""


def add_exception_handlers(app: FastAPI) -> None:
    add_storage_exception_handlers(app)
