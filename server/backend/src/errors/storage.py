from fastapi import FastAPI, Request, Response
from tortoise.exceptions import BaseORMException, DoesNotExist

DBException = BaseORMException
RecordNotFoundException = DoesNotExist


def add_storage_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RecordNotFoundException)
    async def record_not_found_exception_handler(
        _request: Request, _exc: RecordNotFoundException
    ) -> Response:
        return Response(status_code=404)

    @app.exception_handler(DBException)
    async def db_exception_handler(_request: Request, _exc: DBException) -> Response:
        return Response(status_code=500)
