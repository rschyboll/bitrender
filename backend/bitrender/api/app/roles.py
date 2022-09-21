"""Contains users router definition and its routes."""

from fastapi import APIRouter, Depends

from bitrender.api.deps.user import UserContext
from bitrender.api.inject import InjectInRoute
from bitrender.models import Role
from bitrender.schemas import ListRequestInput, RoleView
from bitrender.services.app import IRoleService

from .responses.roles import roles_get_list

roles_router = APIRouter(prefix="/roles")


@roles_router.get("", responses=roles_get_list)
async def get_list(
    request_input: ListRequestInput[Role.columns],
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> list[RoleView]:
    """Returns a list of roles, that are present in the system.

    Allows to specify list request parameters, that allow to sort, search and limit the list
    Additional information present in the description of the ListRequestInput schema.

    When the user has no access to view roles or permissions, the server responds with a 401 status\
         code and a NOT_AUTHORIZED error code."""
    return await role_service.get_list(request_input)
