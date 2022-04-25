"""TODO generate docstring"""

from enum import Enum


class AclAction(Enum):
    """TODO generate docstring"""

    CREATE = "create"
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class AclPermit(Enum):
    """Enum containing available actions."""

    ALLOW = "Allow"
    DENY = "Deny"
    NOTALLOW = "NotAllow"
    NOTDENY = "NotDeny"


AclId = str

AclEntry = tuple[AclPermit, list[AclId] | AclId, list[AclAction] | AclAction]

AclList = list[AclEntry]

EVERYONE = "system:everyone"
AUTHENTICATED = "system:authenticated"
SUPERUSER = "system:superuser"


class StaticAclEntries:
    """Class containing static AclEntries."""

    IS_AUTHENTICATED = (
        AclPermit.NOTDENY,
        AUTHENTICATED,
        [AclAction.CREATE, AclAction.VIEW, AclAction.EDIT, AclAction.DELETE],
    )
    IS_SUPERUSER = (
        AclPermit.ALLOW,
        SUPERUSER,
        [AclAction.CREATE, AclAction.VIEW, AclAction.EDIT, AclAction.DELETE],
    )
