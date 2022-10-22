"""Contains the interface for the role service"""
from abc import abstractmethod

from antidote import interface

from bitrender.models import Role
from bitrender.schemas import ListRequestInput, ListRequestOutput, RoleView


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
