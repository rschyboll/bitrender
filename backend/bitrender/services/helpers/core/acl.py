"""Contains implementation for the IPasswordHelper interface."""

from typing import Sequence, Type

from antidote import implements

from bitrender.core.acl import AclAction, AclEntry, AclList, AclPermit, AclResource
from bitrender.services.helpers.interfaces.acl import IACLHelper


@implements(IACLHelper)
class AclHelper(IACLHelper):
    """Class for validating access to a resource with a control list."""

    def static(
        self,
        resource_types: Sequence[Type[AclResource]],
        actions: AclAction | Sequence[AclAction],
        auth_ids: Sequence[str],
    ) -> bool | None:
        if isinstance(actions, AclAction):
            actions = [actions]
        permits: list[AclPermit | None] = []
        for resource_type in resource_types:
            acl_list = resource_type.__sacl__()
            for action in actions:
                permit = self.__get_acllist_permit(auth_ids, acl_list, action)
                if permit == AclPermit.DENY:
                    return False
                permits.append(permit)
        if all(permit == AclPermit.ALLOW for permit in permits) and len(permits) != 0:
            return True
        return None

    async def dynamic(
        self,
        resources: AclResource | Sequence[AclResource],
        actions: AclAction | Sequence[AclAction],
        auth_ids: Sequence[str],
    ) -> bool | None:
        if isinstance(actions, AclAction):
            actions = [actions]
        if not isinstance(resources, Sequence):
            resources = [resources]
        permits: list[AclPermit | None] = []
        for resource in resources:
            acl_lists = await resource.__dacl__()
            for acl_list in acl_lists:
                for action in actions:
                    permit = self.__get_acllist_permit(auth_ids, acl_list, action)
                    if permit == AclPermit.DENY:
                        return False
                    permits.append(permit)
        if all(permit == AclPermit.ALLOW for permit in permits) and len(permits) != 0:
            return True
        return None

    def __get_acllist_permit(
        self, auth_ids: Sequence[str], acl_list: AclList, required_action: AclAction
    ) -> AclPermit | None:
        for entry in acl_list:
            permit = self.__get_acl_permit(auth_ids, entry, required_action)
            if permit is not None:
                return permit
        return None

    def __get_acl_permit(
        self, auth_ids: Sequence[str], entry: AclEntry, required_action: AclAction
    ) -> AclPermit | None:
        permit = entry[0]
        required_auth_ids = entry[1]
        actions = entry[2]
        if not isinstance(required_auth_ids, list):
            required_auth_ids = [required_auth_ids]
        if not isinstance(actions, list):
            actions = [actions]
        if permit == AclPermit.NOTALLOW:
            if required_action in actions and all(
                auth_id not in auth_ids for auth_id in required_auth_ids
            ):
                return AclPermit.ALLOW
        if permit == AclPermit.NOTDENY:
            if required_action in actions and all(
                auth_id not in auth_ids for auth_id in required_auth_ids
            ):
                return AclPermit.DENY
        if required_action in actions and all(auth_id in auth_ids for auth_id in required_auth_ids):
            return permit
        return None
