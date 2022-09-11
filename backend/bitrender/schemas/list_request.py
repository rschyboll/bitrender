"""Contains schemas for list requests"""

from datetime import datetime
from enum import Enum, unique
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

COLUMNS = TypeVar("COLUMNS", bound=str)


@unique
class SortOrder(Enum):
    """Enum describing the sort order in list requests"""

    ASC = 0
    DESC = 1


@unique
class SearchRule(Enum):
    """Enum describing how to search for a provided value"""

    EQUAL = 0
    NOTEQUAL = 1
    BEGINSWITH = 2
    GREATER = 3
    GREATEROREQUAL = 4
    LESS = 5
    LESSOREQUAL = 6


class ListRequestSort(GenericModel, Generic[COLUMNS]):
    """Schema used in list requests, describes how to sort the requested data

    Attributes:
        column (COLUMNS): By which column the data should be sorted
        order (SortOrder): In what direction the data should be sorted"""

    column: COLUMNS
    order: SortOrder


class ListRequestSearch(GenericModel, Generic[COLUMNS]):
    """Schema used in list requests, used to search for values in specific column

    Attributes:
        column (COLUMNS): By which column the data should be searched
        rule (SearchRule): Rule describing how to search for the value
        values (list[UUID | datetime | int | str | None]): Values to search for in the column"""

    column: COLUMNS
    rule: SearchRule
    value: UUID | datetime | int | str | None


class ListRequestPage(BaseModel):
    """Schema used in list requests, used to define how many records to load and with what offset

    Attributes:
        count (int): How many records should be loaded
        page (int): Page in the list of the records"""

    records_per_page: int
    nr: int


class ListRequestInput(GenericModel, Generic[COLUMNS]):
    """Schema used in list requests, used to define, how and what records should be loaded

    Attributes:
        sort (ListRequestSort[COLUMNS] | None): How the loaded records should be sorted
        search (list[ListRequestSearch[COLUMNS] | None): Search rules for the loaded records
        count: (ListRequestCount | None): How many and with what offset should the records be loaded
    """

    sort: ListRequestSort[COLUMNS] | None
    search: list[ListRequestSearch[COLUMNS]] | None
    page: ListRequestPage | None
