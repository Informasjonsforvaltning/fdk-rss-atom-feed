from fdk_rss_atom_feed.model import (
    SearchOperation,
)
from fdk_rss_atom_feed.query import construct_query
import pytest


@pytest.mark.unit
@pytest.mark.skip(reason="reactivate when integration with search service is succesful")
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
        # filters=Filters(
        #     openData=SearchFilter[bool](value=True),
        #     orgPath=SearchFilter[str](value="987654321"),
        #     accessRights=SearchFilter[str](value="PUBLIC"),
        #     dataTheme=SearchFilter[List[str]](value=["AGRI", "GOVE"]),
        #     losTheme=SearchFilter[List[str]](value=["theme1", "theme2"]),
        #     spatial=SearchFilter[List[str]](value=["Oslo"]),
        #     provenance=SearchFilter[str](value="PROVENANCE"),
        #     formats=None,
        #     uri=None,
        #     lastXDays=None,
        # ),
        # fields=Fields(title=True, description=True, keyword=True),
    )
    assert (
        construct_query(search_string=query.get("query", ""), params=query) == expected
    )


@pytest.mark.unit
@pytest.mark.skip(reason="reactivate when integration with search service is succesful")
def test_construct_query_only_query_text() -> None:
    query = {
        "query": "test query",
    }
    expected = SearchOperation(
        query="test query",
        # filters=Filters(
        #     openData=None,
        #     orgPath=None,
        #     accessRights=None,
        #     dataTheme=None,
        #     losTheme=None,
        #     spatial=None,
        #     provenance=None,
        #     formats=None,
        #     uri=None,
        #     lastXDays=None,
        # ),
        # fields=Fields(title=True, description=True, keyword=True),
    )
    assert construct_query(query.get("query", ""), query) == expected
