import json
import pytest

from fdk_rss_atom_feed.model import Fields, Filters, SearchFilter, SearchOperation
from fdk_rss_atom_feed.query import construct_query


@pytest.mark.unit
def test_json_serialization() -> None:
    searchOp = SearchOperation(
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

    expected = """
        {
            "query": "test query",
            "openData": { "value": true },
            "orgPath": { "value": "987654321" },
            "accessRights": { "value": "PUBLIC" },
            "dataTheme": { "value": ["AGRI", "GOVE"] },
            "losTheme": { "value": ["theme1", "theme2"] },
            "spatial": { "value": ["Oslo"] },
            "provenance": { "value": "PROVENANCE" },
            "formats": null,
            "uri": null,
            "lastXDays": null,
            "fields": {
                "title": true,
                "description": true,
                "keyword": true
            }
        }
    """

    assert json.loads(searchOp.model_dump_json()) == json.loads(expected)
