from typing import Sequence, Type, TypeVar

from bitrender.auth.acl import AclAction, AclEntry, AclList, AclPermit
from bitrender.models.base import BaseModel

ReturnT = TypeVar("ReturnT", bound=BaseModel)


class AclHelper:
    """TODO generate docstring."""

    def __init__(self, auth_ids: list[str]):
        self.auth_ids = auth_ids

    def static_check(
        self, models: Sequence[Type[BaseModel]], actions: AclAction | Sequence[AclAction]
    ) -> bool | None:
        """TODO generate docstring"""
        if isinstance(actions, AclAction):
            actions = [actions]
        permits: list[AclPermit | None] = []
        for model_type in models:
            acl_list = model_type.__sacl__()
            if acl_list is None:
                continue
            for action in actions:
                permit = self.__get_acllist_permit(acl_list, action)
                if permit == AclPermit.DENY:
                    return False
                permits.append(permit)
        if all(permit == AclPermit.ALLOW for permit in permits):
            return True
        return None

    async def dynamic_check(
        self, models: BaseModel | Sequence[BaseModel], actions: AclAction | Sequence[AclAction]
    ) -> bool | None:
        """TODO generate docstring"""
        if isinstance(actions, AclAction):
            actions = [actions]
        if isinstance(models, BaseModel):
            models = [models]
        permits: list[AclPermit | None] = []
        for model in models:
            acl_lists = await model.__dacl__()
            for acl_list in acl_lists:
                for action in actions:
                    permit = self.__get_acllist_permit(acl_list, action)
                    if permit == AclPermit.DENY:
                        return False
                    permits.append(permit)
        if all(permit == AclPermit.ALLOW for permit in permits):
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
                auth_id not in self.auth_ids for auth_id in auth_ids
            ):
                return AclPermit.ALLOW
        if permit == AclPermit.NOTDENY:
            if required_action in actions and all(
                auth_id not in self.auth_ids for auth_id in auth_ids
            ):
                return AclPermit.DENY
        if required_action in actions and all(auth_id in self.auth_ids for auth_id in auth_ids):
            return permit
        return None
