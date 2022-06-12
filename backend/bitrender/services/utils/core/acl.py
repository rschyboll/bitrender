"""Contains implementation for the IPasswordHelper interface."""

from typing import Sequence, Type

from antidote import implements

from bitrender.core.acl import AclAction, AclEntry, AclList, AclPermit, AclResource
from bitrender.models.base import BaseModel
from bitrender.services.utils.interfaces.acl import IACLHelper


@implements(IACLHelper).by_default
class AclHelper(IACLHelper):
    """Class for validating access to a resource with a control list."""

    def static(
        self,
        resources: Sequence[Type[AclResource]],
        actions: AclAction | Sequence[AclAction],
        auth_ids: list[str],
    ) -> bool | None:
        pass

    async def dynamic(
        self,
        resources: AclResource | Sequence[AclResource],
        actions: AclAction | Sequence[AclAction],
        auth_ids: list[str],
    ) -> bool | None:
        if isinstance(actions, AclAction):
            actions = [actions]
        if isinstance(resources, BaseModel):
            resources = [resources]
        permits: list[AclPermit | None] = []
        for model in models:
            acl_lists = await model.__dacl__()
            for acl_list in acl_lists:
                for action in actions:
                    permit = self.__get_acllist_permit(acl_list, action)
                    if permit == AclPermit.DENY:
                        return False
                    permits.append(permit)
        if all(permit == AclPermit.ALLOW for permit in permits) and len(permits) != 0:
            return True
        return None

    def __get_acllist_permit(
        self, acl_list: AclList, required_action: AclAction
    ) -> AclPermit | None:
        for entry in acl_list:
            permit = self.__get_acl_permit(entry, required_action)
            if permit is not None:
                return permit
        return None

    def __get_acl_permit(self, entry: AclEntry, required_action: AclAction) -> AclPermit | None:
        permit = entry[0]
        auth_ids = entry[1]
        actions = entry[2]
        if not isinstance(auth_ids, list):
            auth_ids = [auth_ids]
        if not isinstance(actions, list):
            actions = [actions]
        if permit == AclPermit.NOTALLOW:
            if required_action in actions and all(
                auth_id not in self.__auth_ids for auth_id in auth_ids
            ):
                return AclPermit.ALLOW
        if permit == AclPermit.NOTDENY:
            if required_action in actions and all(
                auth_id not in self.__auth_ids for auth_id in auth_ids
            ):
                return AclPermit.DENY
        if required_action in actions and all(auth_id in self.__auth_ids for auth_id in auth_ids):
            return permit
        return None
