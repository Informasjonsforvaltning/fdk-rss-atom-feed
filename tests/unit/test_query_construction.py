from typing import List

from fdk_rss_atom_feed.config import MAX_SEARCH_HITS
from fdk_rss_atom_feed.model import (
    Filters,
    Pagination,
    SearchFilter,
    SearchOperation,
    Sort,
)
from fdk_rss_atom_feed.query import construct_query
import pytest


@pytest.mark.unit
def test_construct_query() -> None:
    query = {
        "query": "test query",
        "losTheme": "theme1,theme2",
        "dataTheme": "AGRI,GOVE",
        "openData": "true",
        "accessRights": "PUBLIC",
        "orgPath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
    }
    expected = SearchOperation(
        query="test query",
        filters=Filters(
            openData=SearchFilter[bool](value=True),
            orgPath=SearchFilter[str](value="987654321"),
            accessRights=SearchFilter[str](value="PUBLIC"),
            dataTheme=SearchFilter[List[str]](value=["AGRI", "GOVE"]),
            losTheme=SearchFilter[List[str]](value=["theme1", "theme2"]),
            spatial=SearchFilter[List[str]](value=["Oslo"]),
            provenance=SearchFilter[str](value="PROVENANCE"),
            formats=None,
            uri=None,
            lastXDays=None,
            lastXDaysModified=None,
        ),
        sort=Sort(field="FIRST_HARVESTED", direction="DESC"),
        pagination=Pagination(page=0, size=MAX_SEARCH_HITS),
    )
    assert (
        construct_query(search_string=query.get("query", ""), params=query) == expected
    )


@pytest.mark.unit
def test_construct_query_only_query_text() -> None:
    query = {
        "query": "test query",
    }
    expected = SearchOperation(
        query="test query",
        filters=Filters(
            openData=None,
            orgPath=None,
            accessRights=None,
            dataTheme=None,
            losTheme=None,
            spatial=None,
            provenance=None,
            formats=None,
            uri=None,
            lastXDays=None,
            lastXDaysModified=None,
        ),
        sort=Sort(field="FIRST_HARVESTED", direction="DESC"),
        pagination=Pagination(page=0, size=MAX_SEARCH_HITS),
    )
    assert construct_query(query.get("query", ""), query) == expected


@pytest.mark.unit
def test_construct_query_ignores_sort_params() -> None:
    query = {"query": "test", "sortDirection": "ASC", "sortField": "MODIFIED"}
    result = construct_query(search_string="test", params=query)
    assert result.sort == Sort(field="FIRST_HARVESTED", direction="DESC")


@pytest.mark.unit
def test_construct_query_with_last_x_days() -> None:
    query = {"query": "test", "lastXDays": "7", "lastXDaysModified": "30"}
    result = construct_query(search_string="test", params=query)
    assert result.filters is not None
    assert result.filters.lastXDays == SearchFilter[int](value=7)
    assert result.filters.lastXDaysModified == SearchFilter[int](value=30)
