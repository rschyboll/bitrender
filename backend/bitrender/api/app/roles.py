"""Contains users router definition and its routes."""


from uuid import UUID

from fastapi import APIRouter, Depends

from bitrender.api.deps.user import UserContext, get_current_user
from bitrender.api.inject import InjectInRoute
from bitrender.models import Role
from bitrender.schemas import ListRequestInput, ListRequestOutput, RoleCreate, RoleView
from bitrender.services.app import IRoleService

from .responses.roles import roles_get_by_id, roles_get_list

roles_router = APIRouter(prefix="/roles")


@roles_router.get(
    "",
    dependencies=[Depends(get_current_user)],
    responses=roles_get_list,
    response_model=ListRequestOutput[RoleView],
)
async def get_list(
    request_input: ListRequestInput[Role.columns] = Depends(
        ListRequestInput[Role.columns].create_dependency(Role.columns)
    ),
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> ListRequestOutput[RoleView]:
    """Returns a list of roles, that are present in the system.

    Allows to specify list request parameters, that allow to sort, search and limit the list
    Additional information present in the description of the ListRequestInput schema.

    When the user has no access to view roles or permissions, the server responds with a 401 status\
         code and a NOT_AUTHORIZED error code."""
    return await role_service.get_list(request_input)


@roles_router.post(
    "/new",
    dependencies=[
        Depends(get_current_user),
    ],
)
async def create(
    role_data: RoleCreate,
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> RoleView:
    """Creates a new role.

    When a role exists with the given name, \
        the server responds with a 409 status code and a ROLE_NAME_TAKEN error code.

    Whem the user has no permission to create roles, \
        the server responds with a 401 status code and a NOT_AUTHORIZED error code."""

    return await role_service.create(role_data)


@roles_router.get(
    "/{role_id}",
    dependencies=[Depends(get_current_user)],
    responses=roles_get_by_id,
    response_model=RoleView,
)
async def get_by_id(
    role_id: UUID,
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> RoleView:
    """Returns a role based on the provided role_id.

    When the user has no access to the role or it's permissions, \
        the server responds with a 401 status code and a NOT_AUTHORIZED error code."""
    return await role_service.get_by_id(role_id)
