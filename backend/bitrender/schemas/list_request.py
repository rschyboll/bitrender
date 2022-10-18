"""Contains schemas for list requests"""
from __future__ import annotations

from typing import Any, Callable, Generic, Optional, TypeVar
from uuid import UUID

from fastapi import Depends, Query
from pydantic import BaseModel, root_validator
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

    @classmethod
    def from_query(
        cls,
        column: COLUMNS_co | None = Query(None),
        order: SortOrder | None = Query(None),
    ) -> ListRequestSort[COLUMNS_co] | None:
        """Creates the schema from optional query parameters. Fastapi dependency.

        Args:
            column (COLUMNS_co | None, optional): Optional column, same as class attribute.
                Defaults to Query(None).
            order (SortOrder | None, optional): Optional order, same as class attribute.
                Defaults to Query(None).

        Returns:
            ListRequestSort[COLUMNS_co] | None: Instance of the class, or None if not all \
                attributes were provided."""
        if column is None or order is None:
            return None
        else:
            return cls(column=column, order=order)


class ListRequestSearch(GenericModel, Generic[COLUMNS_co]):
    """Schema used in list requests, used to search for values in specific column

    Attributes:
        column (COLUMNS): By which column the data should be searched
        rule (SearchRule): Rule describing how to search for the value
        value (UUID | datetime | int | str | None): Value to search for in the column"""

    column: COLUMNS_co
    rule: SearchRule
    value: UUID | int | str | None


class ListRequestSearchInput(GenericModel, Generic[COLUMNS_co]):
    """Schema used as an input, for the ListRequestSearch schema. Required for query requests.

    Attributes:
        column (list[COLUMNS]): By which column the data should be searched
        rule (list[SearchRule]): Rule describing how to search for the value
        values (list[UUID | datetime | int | str | None]): Values to search for in the column"""

    column: Optional[list[COLUMNS_co]]
    rule: Optional[list[SearchRule]]
    value: Optional[list[UUID | int | str | None]]

    def to_list(self) -> list[ListRequestSearch[COLUMNS_co]]:
        """Converts the schema to a list of ListRequestSearch schemas.

        Returns:
            list[ListRequestSearch[COLUMNS_co]]: List of ListRequestSearch."""
        search_list: list[ListRequestSearch[COLUMNS_co]] = []
        i = 0
        if self.column is not None and self.rule is not None and self.value is not None:
            for column in self.column:
                rule = self.rule[i]
                value = self.value[i]
                search_list.append(ListRequestSearch(column=column, rule=rule, value=value))
                i += 1
        return search_list

    @classmethod
    def from_query(
        cls,
        search_column: list[COLUMNS_co] | None = Query(None),
        search_rule: list[int] | None = Query(None),
        search_value: list[UUID | int | str | None] | None = Query(None),
    ) -> ListRequestSearchInput[COLUMNS_co]:
        """TODO generate docstring"""
        return cls(column=search_column, rule=search_rule, value=search_value)

    @root_validator(pre=True)
    @classmethod
    def lists_length_must_be_equal(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validates, that that the arrays, from the query, have the same number of values.

        Args:
            values (dict[str, Any]): Values to validate.

        Returns:
            dict[str, Any]: Validated values."""
        if (
            ("column" not in values or values["column"]) is None
            or ("rule" not in values or values["rule"] is None)
            or ("value" not in values or values["value"] is None)
        ):
            return values
        if len(values["column"]) != len(values["rule"]) or len(values["value"]) != len(
            values["value"]
        ):
            raise ValueError(
                "Search query args require the same number of values for each property."
            )
        return values


class ListRequestPage(BaseModel):
    """Schema used in list requests, used to define how many records to load and with what offset

    Attributes:
        count (int): How many records should be loaded
        page (int): Page in the list of the records"""

    records_per_page: int
    page_nr: int

    @classmethod
    def from_query(
        cls,
        records_per_page: int | None = Query(None),
        page_nr: int | None = Query(None),
    ) -> ListRequestPage | None:
        """TODO generate docstring"""
        if records_per_page is None or page_nr is None:
            return None
        return cls(records_per_page=records_per_page, page_nr=page_nr)


class ListRequestInput(GenericModel, Generic[COLUMNS_co]):
    """Schema used in list requests, used to define, how and what records should be loaded

    Attributes:
        sort (ListRequestSort[COLUMNS] | None): How the loaded records should be sorted
        search (list[ListRequestSearch[COLUMNS] | None): Search rules for the loaded records
        count: (ListRequestCount | None): How many and with what offset should the records be loaded
    """

    sort: Optional[ListRequestSort[COLUMNS_co]] = None
    search: list[ListRequestSearch[COLUMNS_co]] = []
    page: Optional[ListRequestPage] = None

    @classmethod
    def create_dependency(cls, columns: object) -> Callable[..., ListRequestInput[COLUMNS_co]]:
        """_summary_

        Args:
            columns (object): _description_

        Returns:
            Callable[..., ListRequestInput[COLUMNS_co]]: _description_"""
        Sort = type("Sort", (ListRequestSort[columns],), {})  # type: ignore
        Search = type("Search", (ListRequestSearchInput[columns],), {})  # type: ignore
        # pylint: disable=no-member

        def dependency(
            search: ListRequestSearchInput[COLUMNS_co] = Depends(Search.from_query),  # type: ignore
            sort: ListRequestSort[COLUMNS_co] | None = Depends(Sort.from_query),  # type: ignore
            page: ListRequestPage = Depends(ListRequestPage.from_query),
        ) -> ListRequestInput[COLUMNS_co]:
            return ListRequestInput(search=search.to_list(), sort=sort, page=page)

        # pylint: enable=no-member
        return dependency
