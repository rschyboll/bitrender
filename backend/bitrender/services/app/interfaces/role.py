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
        """Returns a list of roles based on the given request parameters.

        Args:
            request_input (ListRequestInput[Role.columns]): Contains search, order, and
                page parameters.

        Raises:
            UnauthorizedError: The user does not have access to view roles or
                permissions.

        Returns:
            ListRequestOutput[RoleView]: A list of `RoleView` objects, containing the
                requested roles."""

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> RoleView:
        """Returns a role with the given ID.

        Args:
            role_id (UUID): ID of the requested role.

        Raises:
            UnauthorizedError: The user does not have access to view this role.
            DoesNotExist: The role does not exist.

        Returns:
            RoleView: The requested role."""

    @abstractmethod
    async def get_multiple(self, role_ids: list[UUID]) -> list[RoleView]:
        """Returns multiple roles with the given IDs.

        Args:
            role_ids (list[UUID]): List of IDs of the requested roles.

        Raises:
            UnauthorizedError: The user does not have access to view these roles.
            DoesNotExist: One or more of the roles do not exist.

        Returns:
            list[RoleView]: A list of `RoleView` objects, containing the requested roles."""

    @abstractmethod
    async def get_role_users_count(self, role_id: UUID) -> int:
        """Returns the number of users who have the given role assigned.

        Args:
            role_id (UUID): ID of the role.

        Raises:
            UnauthorizedError: The user does not have access to view this role.
            DoesNotExist: The role does not exist.

        Returns:
            int: The number of users who have this role assigned."""

    @abstractmethod
    async def create(self, role_data: RoleCreate) -> RoleView:
        """Creates a new role with the given data.

        Args:
            role_data (RoleCreate): Data required to create the role.

        Raises:
            UnauthorizedError: The user does not have access to create new roles.
            RoleNameTaken: A role with the same name already exists.

        Returns:
            RoleView: The created role."""

    @abstractmethod
    async def delete(
        self,
        role_id: UUID,
        replacement_role_id: UUID | None,
    ) -> None:
        """Deletes the role with the given ID.

        Args:
            role_id (UUID): ID of the role that should be deleted.
            replacement_role_id (UUID | None): ID of the role to be assigned to users who
                currently have the role being deleted. If no replacement role is provided,
                users will not be assigned any new role.

        Raises:
            UnauthorizedError: The user does not have access to delete this role.
            DoesNotExist: The role does not exist.
            RoleIsDefault: The role is the current default one and cannot be removed."""
