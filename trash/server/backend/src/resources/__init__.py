from fastapi import FastAPI, Request, exceptions
from fastapi.responses import Response
from starlette.exceptions import HTTPException
from storage import NotFoundException


def add_resource_exception_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundException, __handle_not_found_exception)

async def __handle_not_found_exception(request: Request, exception: NotFoundException):
    return Response(status_code=404)
