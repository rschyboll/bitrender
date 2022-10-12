"""Contains tests for the schemas in bitrender.schemas.list_request."""
from bitrender.enums.list_request import SearchRule, SortOrder
from bitrender.schemas.list_request import ListRequestSearchInput, ListRequestSort


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
        """Tests that the to_list method correctly converts it's properties to a list of\
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

    def test_to_list_with_none_values(self) -> None:
        pass
