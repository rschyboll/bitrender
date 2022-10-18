"""Contains tests for the schemas in bitrender.schemas.list_request."""
from typing import Literal
from uuid import UUID

import pytest

from bitrender.enums.list_request import SearchRule, SortOrder
from bitrender.schemas.list_request import (
    ListRequestInput,
    ListRequestPage,
    ListRequestSearchInput,
    ListRequestSort,
)


class TestListRequestSort:
    """Contains tests for the ListRequestSort schema."""

    def test_from_query(self) -> None:
        """Tests that the from_query method correctly creates an instance of the schema."""
        column = "test"
        order = SortOrder.ASC
        list_request_sort = ListRequestSort.from_query(column, order)
        assert list_request_sort is not None
        assert column == list_request_sort.column
        assert order == list_request_sort.order

    def test_from_query_returns_none(self) -> None:
        """Tests that the from_query method correctly returns None if some of it args are None."""
        assert ListRequestSort.from_query("", None) is None
        assert ListRequestSort.from_query(None, SortOrder.ASC) is None
        assert ListRequestSort.from_query(None, None) is None


class TestListRequestSearchInput:
    """Contains tests for the ListRequestSearchInput schema."""

    def test_to_list(self) -> None:
        """Tests that the to_list method correctly converts it's attributes to a list of\
             ListRequestSearch class."""
        columns = ["1", "2", "3", "4", "5"]
        rules = [
            SearchRule.BEGINSWITH,
            SearchRule.EQUAL,
            SearchRule.LESS,
            SearchRule.NOTEQUAL,
            SearchRule.LESSOREQUAL,
        ]
        values = [1, 2, 3, 4, 5]
        list_request_search_input = ListRequestSearchInput[str](
            column=columns, rule=rules, value=values
        )
        list_request_search_list = list_request_search_input.to_list()
        assert len(list_request_search_list) == len(columns)
        for list_request_search in list_request_search_list:
            assert list_request_search.column in columns
            assert list_request_search.rule in rules
            assert list_request_search.value in values

    def test_to_list_with_none_values(self) -> None:
        """Tests that the to_list method returns an empty array, \
            if one or more attributes are None."""
        list_request_search_input = ListRequestSearchInput[str]()
        list_request_search_list = list_request_search_input.to_list()
        assert len(list_request_search_list) == 0

    def test_from_query(self) -> None:
        """Tests that the from_query method creates an instance of the class,\
             with the correct values."""
        search_columns = ["1", "2", "3"]
        search_rules: list[int] = [SearchRule.BEGINSWITH, SearchRule.GREATER, SearchRule.LESS]
        search_values: list[int | str | UUID | None] = [1, 2, 3]
        list_request_search_input = ListRequestSearchInput[str].from_query(
            search_columns, search_rules, search_values
        )
        assert search_columns == list_request_search_input.column
        assert search_rules == list_request_search_input.rule
        assert search_values == list_request_search_input.value

    def test_lists_length_must_be_equal(self) -> None:
        """Tests that the method raises ValueError on wrong values."""
        assert ListRequestSearchInput.lists_length_must_be_equal(values={"column": None}) == {
            "column": None
        }
        assert ListRequestSearchInput.lists_length_must_be_equal(
            values={
                "column": ["id"],
                "rule": [SearchRule.BEGINSWITH],
                "value": [1],
            }
        ) == {
            "column": ["id"],
            "rule": [SearchRule.BEGINSWITH],
            "value": [1],
        }
        with pytest.raises(ValueError):
            ListRequestSearchInput.lists_length_must_be_equal(
                values={
                    "column": ["id", "id2"],
                    "rule": [SearchRule.BEGINSWITH],
                    "value": [1, 3],
                }
            )


class TestListRequestPage:
    """Contains tests for the ListRequestPage schema."""

    def test_from_query(self) -> None:
        """Tests that the from_query method correctly creates an instance of the schema."""
        page_nr = 1
        records_per_page = 1
        list_request_page = ListRequestPage.from_query(1, 1)
        assert list_request_page is not None
        assert list_request_page.records_per_page == records_per_page
        assert list_request_page.page_nr == page_nr

    def test_from_query_returns_none(self) -> None:
        """Tests that the from_query method correctly returns None if some of it args are None."""
        assert ListRequestPage.from_query(1, None) is None
        assert ListRequestPage.from_query(None, 1) is None
        assert ListRequestPage.from_query(None, None) is None


class TestListRequestInput:
    """Contains tests for the ListRequestInput schema."""

    def test_create_dependency(self) -> None:
        """Tests that the create_dependency method returns\
             a function that creates an instance of the schema."""
        list_request_page = ListRequestPage(records_per_page=1, page_nr=1)
        dependency = ListRequestInput[Literal["id", "id2"]].create_dependency(Literal["id", "id2"])
