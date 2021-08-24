from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import exception_view_config
from sqlalchemy.exc import OperationalError

from . import StatusCodes


@exception_view_config(OperationalError, renderer='json')
def database_critical_error(exc: OperationalError, request: Request) -> Response:
    response = Response()
    response.json_body = {'statusCode': StatusCodes.DATABASE_ERROR}
    response.status_int = 500
    return response