"""Contains interface for the acl helper implementations."""
from abc import ABC
from typing import Sequence, Type

from antidote import interface
from pyparsing import abstractmethod

from bitrender.core.acl import AclAction, AclResource


@interface
class IACLHelper(ABC):
    """Interface for classes for validating access to a resource with a control list."""

    @abstractmethod
    def static(
        self,
        resources: Sequence[Type[AclResource]],
        actions: AclAction | Sequence[AclAction],
        auth_ids: list[str],
    ) -> bool | None:
        """Checks if provided auth_ids fulfil the static acl of the provided resources.

        Args:
            resources (Sequence[Type[AclResource]]): Resources with the static acl list.
            actions (AclAction | Sequence[AclAction]): Actions which access needs to be checked.
            auth_ids (list[str]): Authentication id's of the entity requiring the access.

        Returns:
            bool | None: True if the access is granted, false if denied, none if could not be \
                specified."""

    @abstractmethod
    async def dynamic(
        self,
        resources: AclResource | Sequence[AclResource],
        actions: AclAction | Sequence[AclAction],
        auth_ids: list[str],
    ) -> bool | None:
        """Checks if provided auth_ids fulfil the dynamic acl of the provided resources.

        Args:
            resources (AclResource | Sequence[AclResource]):  Resources with the dynamic acl list.
            actions (AclAction | Sequence[AclAction]): Actions which access needs to be checked.
            auth_ids (list[str]): Authentication id's of the entity requiring the access.

        Returns:
            bool | None: True if the access is granted, false if denied, none if could not be \
                specified."""
