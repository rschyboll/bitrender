"""Contains the interface for the role service"""
from abc import abstractmethod
from uuid import UUID

from antidote import interface

from bitrender.models import Role
from bitrender.schemas import ListRequestInput, ListRequestOutput, RoleCreate, RoleView


@interface
class IRoleService:
    """Service used for operation on user roles and permissions"""

    @abstractmethod
    async def get_list(
        self, request_input: ListRequestInput[Role.columns]
    ) -> ListRequestOutput[RoleView]:
        """Returns a list of roles based on the request_input parameter
        Allows for searching, ordering and requesting a specific amount of roles

        Args:
            request_input (ListRequestInput[Role.columns]): Contains the search, \
                order and amount parameters

        Raises:
            UnauthorizedError: The user has no access to view roles or permissions

        Returns:
            ListRequestOutput[RoleView]: Schema with a list of RoleView schemas, \
                containing the requested roles"""

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> RoleView:
        """Returns a role with the provided id.

        Args:
            role_id (UUID): Id of the requested role

        Raises:
            UnauthorizedError: The user has no access to view this role.

        Returns:
            RoleView: The requested role."""

    @abstractmethod
    async def create(self, role_data: RoleCreate) -> RoleView:
        """Creates a new role.

        Args:
            role_data (RoleCreate): Data required to create the role.

        Raises:
            UnauthorizedError: The user has no access to create new roles.
            RoleNameTaken: A role with the name already exists.

        Returns:
            RoleView: The created role."""
