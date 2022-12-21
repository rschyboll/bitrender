"""Contains schemas for list requests"""
from __future__ import annotations

from typing import Any, Callable, Generic, Optional, TypeVar
from uuid import UUID

from fastapi import Depends, Query
from pydantic import BaseModel, root_validator
from pydantic.generics import GenericModel

from bitrender.enums.list_request import SearchRule, SortOrder

COLUMNS_co = TypeVar("COLUMNS_co", bound=str, covariant=True)
RETURNV_co = TypeVar("RETURNV_co", bound=BaseModel, covariant=True)


class ListRequestSort(GenericModel, Generic[COLUMNS_co]):
    """A schema used in list requests to describe how to sort the requested data.

    Attributes:
        column (COLUMNS_co): The column by which the data should be sorted.
        order (SortOrder): The direction in which the data should be sorted.
    """

    column: COLUMNS_co
    order: SortOrder

    @classmethod
    def from_query(
        cls,
        column: COLUMNS_co | None = Query(None),
        order: SortOrder | None = Query(None),
    ) -> ListRequestSort[COLUMNS_co] | None:
        """Creates an instance of the `ListRequestSort` class from optional query parameters.

        This method is a dependency of the FastAPI library.

        Args:
            column (COLUMNS_co | None, optional): An optional column to sort the data by.
                Defaults to `Query(None)`.
            order (SortOrder | None, optional): An optional sort order for the data.
                Defaults to `Query(None)`.

        Returns:
            Union[ListRequestSort[COLUMNS_co], None]: An instance of the `ListRequestSort` class,
            or `None` if both `column` and `order` are not provided.
        """
        if column is None or order is None:
            return None
        else:
            return cls(column=column, order=order)


class ListRequestSearch(GenericModel, Generic[COLUMNS_co]):
    """A schema used in list requests to search for values in a specific column.

    Attributes:
        column (COLUMNS_co): The column by which the data should be searched.
        rule (SearchRule): The rule describing how to search for the value.
        value (Union[UUID, int, str, None]): The value to search for in the column.
    """

    column: COLUMNS_co
    rule: SearchRule
    value: UUID | int | str | None


class ListRequestSearchInput(GenericModel, Generic[COLUMNS_co]):
    """A schema used as an input for the `ListRequestSearch` schema.
        This input is required for query requests.

    Attributes:
        column (Optional[List[COLUMNS_co]]): The columns by which the data \
            should be searched.
        rule (Optional[List[SearchRule]]): The rules describing how to search \
            for the value in each column.
        value (Optional[List[Union[UUID, int, str, None]]]): The values to search \
            for in the columns.
    """

    column: Optional[list[COLUMNS_co]]
    rule: Optional[list[SearchRule]]
    value: Optional[list[UUID | int | str | None]]

    def to_list(self) -> list[ListRequestSearch[COLUMNS_co]]:
        """Converts the schema to a list of `ListRequestSearch` schemas.

        Returns:
            List[ListRequestSearch[COLUMNS_co]]: A list of `ListRequestSearch` instances.
        """
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
        """Creates an instance of the `ListRequestSearchInput` class from query parameters.

        Args:
            search_column (Optional[List[COLUMNS_co]], optional): A list of columns to search.
                Defaults to `Query(None)`.
            search_rule (Optional[List[int]], optional): A list of search rules for each column.
                Defaults to `Query(None)`.
            search_value (Optional[List[Union[UUID, int, str, None]]], optional): \
                A list of values to search for in each column. Defaults to `Query(None)`.

        Returns:
            ListRequestSearchInput[COLUMNS_co]: An instance of the `ListRequestSearchInput` class.
        """
        return cls(column=search_column, rule=search_rule, value=search_value)

    @root_validator(pre=True)
    @classmethod
    def lists_length_must_be_equal(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that the lists of query parameters have the same number of values.

        This method checks if the lists for the parameters 'column', 'rule', and 'value' \
            have the same number of elements.
        If any of these lists are missing or empty, the method will return the values as-is.
        Otherwise, if the lists have different lengths, a ValueError is raised.

        Args:
            values (Dict[str, Any]): The values to validate.

        Returns:
            Dict[str, Any]: The validated values.
        """
        if (
            ("column" not in values or values["column"] is None)
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
    """Schema for defining pagination parameters in a list request.

    This class is used to specify how many records should be loaded and the page number for the \
        list of records.

    Attributes:
        records_per_page (int): The number of records to load.
        page_nr (int): The page number in the list of records.
    """

    records_per_page: int
    page_nr: int

    @classmethod
    def from_query(
        cls,
        records_per_page: int | None = Query(None),
        page_nr: int | None = Query(None),
    ) -> ListRequestPage | None:
        """Create a ListRequestPage instance from query parameters.

        If the 'records_per_page' or 'page_nr' query parameters are not provided, \
            this method returns None.
        Otherwise, it returns a ListRequestPage instance with the provided values for \
            'records_per_page' and 'page_nr'.

        Args:
            records_per_page (int, optional): The number of records to load. Defaults to None.
            page_nr (int, optional): The page number in the list of records. Defaults to None.

        Returns:
            Optional[ListRequestPage]: A ListRequestPage instance with the provided values, \
                or None if either parameter is not provided.
        """
        if records_per_page is None or page_nr is None:
            return None
        return cls(records_per_page=records_per_page, page_nr=page_nr)


class ListRequestRange(BaseModel):
    """Schema for defining a range of records in a list request.

    This class is used to specify a range of records to be loaded in a list request.

    Attributes:
        beginning (int): The index of the first record to be loaded.
        end (int): The index of the last record to be loaded.
    """

    beginning: int
    end: int

    @classmethod
    def from_query(
        cls,
        beginning: int | None = Query(None),
        end: int | None = Query(None),
    ) -> ListRequestRange | None:
        """Create a ListRequestRange instance from query parameters.

        If the 'beginning' or 'end' query parameters are not provided, this method returns None.
        Otherwise, it returns a ListRequestRange instance with the provided values for \
            'beginning' and 'end'.

        Args:
            beginning (int, optional): The index of the first record to be loaded. \
                Defaults to None.
            end (int, optional): The index of the last record to be loaded. \
                Defaults to None.

        Returns:
            Optional[ListRequestRange]: A ListRequestRange instance with the provided values, \
                or None if either parameter is not provided.
        """
        if beginning is None or end is None:
            return None
        return cls(beginning=beginning, end=end)


class ListRequestInput(GenericModel, Generic[COLUMNS_co]):
    """Schema for defining the parameters of a list request.

    Copy code
    This class is used to specify how and what records should be loaded in a list request.

    Attributes:
        sort (Optional[ListRequestSort[COLUMNS]]): How the loaded records should be sorted.
        search (List[ListRequestSearch[COLUMNS]]): Search rules for the loaded records.
        page_or_range (Optional[Union[ListRequestPage, ListRequestRange]]): Pagination parameters \
            for the list of records.
    """

    sort: Optional[ListRequestSort[COLUMNS_co]] = None
    search: list[ListRequestSearch[COLUMNS_co]] = []
    page_or_range: Optional[ListRequestPage | ListRequestRange] = None

    @classmethod
    def create_dependency(cls, columns: object) -> Callable[..., ListRequestInput[COLUMNS_co]]:
        """Create a dependency injection function for a ListRequestInput instance.

        This method creates a function that can be used as a dependency in a FastAPI endpoint.
        The function accepts query parameters for the 'search', 'sort', and 'page_or_range' \
            attributes of a ListRequestInput instance and returns a ListRequestInput instance with\
            these values.

        Args:
            columns (object): The column types for the ListRequestInput instance.

        Returns:
            Callable[[], ListRequestInput[COLUMNS_co]]: A dependency injection function for a \
                ListRequestInput instance.
        """

        Sort = type("Sort", (ListRequestSort[columns],), {})  # type: ignore
        Search = type("Search", (ListRequestSearchInput[columns],), {})  # type: ignore
        # pylint: disable=no-member

        def dependency(
            search: ListRequestSearchInput[COLUMNS_co] = Depends(Search.from_query),  # type: ignore
            sort: ListRequestSort[COLUMNS_co] | None = Depends(Sort.from_query),  # type: ignore
            list_page: ListRequestPage | None = Depends(ListRequestPage.from_query),
            list_range: ListRequestRange | None = Depends(ListRequestRange.from_query),
        ) -> ListRequestInput[COLUMNS_co]:
            if list_page is not None and list_range is not None:
                raise ValueError("Only range or page can be defined in the query.")
            if list_page is not None:
                return ListRequestInput(search=search.to_list(), sort=sort, page_or_range=list_page)
            return ListRequestInput(search=search.to_list(), sort=sort, page_or_range=list_range)

        # pylint: enable=no-member
        return dependency


class ListRequestOutput(GenericModel, Generic[RETURNV_co]):
    """A class representing the output of a successful list request.

    This class contains the results of a list request and the number of rows in the result set.

    Attributes:
        items (List[RETURNV_co]): The resulting items from the list request.
        row_count (int): The number of rows in the result set.
    """

    items: list[RETURNV_co]
    row_count: int
