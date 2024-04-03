from dataclasses import asdict
import json
from typing import List

from fdk_rss_atom_feed.model import Filters, SearchFilter, SearchOperation
import pytest


@pytest.mark.unit
def test_json_serialization() -> None:
    search_operation = SearchOperation(
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
        ),
    )

    expected = """
        {
            "query": "test query",
            "filters": {
                "openData": { "value": true },
                "orgPath": { "value": "987654321" },
                "accessRights": { "value": "PUBLIC" },
                "dataTheme": { "value": ["AGRI", "GOVE"] },
                "losTheme": { "value": ["theme1", "theme2"] },
                "spatial": { "value": ["Oslo"] },
                "provenance": { "value": "PROVENANCE" },
                "formats": null,
                "uri": null,
                "lastXDays": null
            },
            "sort": null,
            "pagination": null
        }
    """.strip()

    assert json.loads(json.dumps(asdict(search_operation))) == json.loads(expected)
