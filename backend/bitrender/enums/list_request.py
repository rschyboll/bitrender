"""Contains enums for list request schemas"""
from enum import IntEnum, unique


@unique
class SortOrder(IntEnum):
    """Enum describing the sort order in list requests"""

    ASC = 0
    DESC = 1


@unique
class SearchRule(IntEnum):
    """Enum describing how to search for a provided value"""

    EQUAL = 0
    NOTEQUAL = 1
    BEGINSWITH = 2
    GREATER = 3
    GREATEROREQUAL = 4
    LESS = 5
    LESSOREQUAL = 6
    CONTAINS = 7
