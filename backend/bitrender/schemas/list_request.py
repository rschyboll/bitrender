"""Contains schemas for list requests"""
from __future__ import annotations

from datetime import datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

from bitrender.enums.list_request import SearchRule, SortOrder

COLUMNS_co = TypeVar("COLUMNS_co", bound=str, covariant=True)


class ListRequestSort(GenericModel, Generic[COLUMNS_co]):
    """Schema used in list requests, describes how to sort the requested data

    Attributes:
        column (COLUMNS): By which column the data should be sorted
        order (SortOrder): In what direction the data should be sorted"""

    column: COLUMNS_co
    order: SortOrder


class ListRequestSearch(GenericModel, Generic[COLUMNS_co]):
    """Schema used in list requests, used to search for values in specific column

    Attributes:
        column (COLUMNS): By which column the data should be searched
        rule (SearchRule): Rule describing how to search for the value
        values (list[UUID | datetime | int | str | None]): Values to search for in the column"""

    column: COLUMNS_co
    rule: SearchRule
    value: UUID | int | str | None


class ListRequestPage(BaseModel):
    """Schema used in list requests, used to define how many records to load and with what offset

    Attributes:
        count (int): How many records should be loaded
        page (int): Page in the list of the records"""

    records_per_page: int
    nr: int


class ListRequestInput(GenericModel, Generic[COLUMNS_co]):
    """Schema used in list requests, used to define, how and what records should be loaded

    Attributes:
        sort (ListRequestSort[COLUMNS] | None): How the loaded records should be sorted
        search (list[ListRequestSearch[COLUMNS] | None): Search rules for the loaded records
        count: (ListRequestCount | None): How many and with what offset should the records be loaded
    """

    sort: Optional[ListRequestSort[COLUMNS_co]]
    search: Optional[list[ListRequestSearch[COLUMNS_co]]]
    page: Optional[ListRequestPage]
