"""TODO generate docstring"""

from enum import Enum


class AclAction(Enum):
    """TODO generate docstring"""

    CREATE = "create"
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class AclPermit(Enum):
    """TODO generate docstring"""

    ALLOW = "Allow"
    DENY = "Deny"
    NOTALLOW = "NotAllow"
    NOTDENY = "NotDeny"


AclEntry = tuple[AclPermit, list[str] | str, list[AclAction] | AclAction]

AclList = list[AclEntry]

EVERYONE = "system:everyone"
AUTHENTICATED = "system:authenticated"


class StaticAclEntries:
    """TODO generate docstring"""

    IS_AUTHENTICATED = (
        AclPermit.NOTDENY,
        AUTHENTICATED,
        [AclAction.CREATE, AclAction.VIEW, AclAction.EDIT, AclAction.DELETE],
    )
