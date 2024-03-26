import pytest

from fdk_rss_atom_feed.model import Fields, Filters, SearchFilter, SearchOperation
from fdk_rss_atom_feed.query import construct_query


@pytest.mark.unit
def test_construct_query() -> None:
    query = {
        "q": "test query",
        "losTheme": "theme1,theme2",
        "theme": "AGRI,GOVE",
        "opendata": "true",
        "accessrights": "PUBLIC",
        "orgPath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
    }
    expected = SearchOperation(
        query="test query",
        filters=Filters(
            openData=SearchFilter(value=True),
            orgPath=SearchFilter(value="987654321"),
            accessRights=SearchFilter(value="PUBLIC"),
            dataTheme=SearchFilter(value=["AGRI", "GOVE"]),
            losTheme=SearchFilter(value=["theme1", "theme2"]),
            spatial=SearchFilter(value=["Oslo"]),
            provenance=SearchFilter(value="PROVENANCE"),
            formats=None,
            uri=None,
            lastXDays=None,
        ),
        fields=Fields(title=True, description=True, keyword=True),
    )
    assert construct_query(search_string=query.get("q", ""), params=query) == expected


@pytest.mark.unit
def test_construct_query_only_query_text() -> None:
    query = {
        "q": "test query",
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
        ),
        fields=Fields(title=True, description=True, keyword=True),
    )
    assert construct_query(query.get("q", ""), query) == expected
