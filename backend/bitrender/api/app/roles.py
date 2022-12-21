"""Contains users router definition and its routes."""


from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

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
    """Endpoint to retrieve a list of roles.

    This endpoint allows the user to specify list request parameters, such as sorting,
    searching, and limiting the list. For more information on the list request parameters,
    see the description of the ListRequestInput schema.

    If the user does not have permission to view roles, the server will respond with a
    401 status code and a NOT_AUTHORIZED error code.
    """
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
    """Endpoint to create a new role.

    If a role with the given name already exists, the server will respond with a
    409 status code and a ROLE_NAME_TAKEN error code.

    If the user does not have permission to create roles, the server will respond
    with a 401 status code and a NOT_AUTHORIZED error code.
    """
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


@roles_router.get("/{role_id}", dependencies=[Depends(get_current_user)])
async def get_multiple(
    role_ids: list[UUID],
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> list[RoleView]:
    return await role_service.get_multiple(role_ids)


@roles_router.delete(
    "/{role_id}",
    dependencies=[Depends(get_current_user)],
)
async def delete(
    role_id: UUID,
    replacement_role_id: UUID | None,
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> None:
    await role_service.delete(role_id, replacement_role_id)


@roles_router.get("/{role_id}/user_count", dependencies=[Depends(get_current_user)])
async def get_user_count(
    role_id: UUID,
    role_service: IRoleService = Depends(InjectInRoute(IRoleService, UserContext, "context")),
) -> int:
    """Returns a role based on the provided role_id.

    When the user has no access to the role or it's permissions, \
        the server responds with a 401 status code and a NOT_AUTHORIZED error code."""
    return await role_service.get_role_users_count(role_id)
