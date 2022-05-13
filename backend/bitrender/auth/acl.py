"""Contains types and enums used for defining acl lists."""

from enum import Enum


class AclAction(str, Enum):
    """Enum containing all available acl actions."""

    CREATE = "create"
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class AclPermit(str, Enum):
    """Enum containing all available acl permits."""

    ALLOW = "Allow"
    """Allows access when the user fulfills the entry."""

    DENY = "Deny"
    """Denies access when the user fulfills the entry."""

    NOTALLOW = "NotAllow"
    """Allows access when the user does not fulfill the entry."""

    NOTDENY = "NotDeny"
    """Denies access when the user does not fulfill the entry."""


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
