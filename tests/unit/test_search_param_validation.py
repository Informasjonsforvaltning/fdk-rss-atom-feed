from fdk_rss_atom_feed.feed import get_search_params
import pytest


@pytest.mark.unit
def test_search_param_validation() -> None:
    """Known params are mapped to canonical names, unknown params are ignored"""
    input = {
        "query": "test query",
        "lostheme": "theme1,theme2",
        "datatheme": "AGRI,GOVE",
        "opendata": "true",
        "accessrights": "PUBLIC",
        "orgpath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
        "formats": "CSV,JSON",
        "sortdirection": "ASC",
        "sortfield": "MODIFIED",
        "unknownparam": "ignored",
        "lastxdays": "7",
        "lastxdaysmodified": "30",
    }

    expected = {
        "query": "test query",
        "losTheme": "theme1,theme2",
        "dataTheme": "AGRI,GOVE",
        "openData": "true",
        "accessRights": "PUBLIC",
        "orgPath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
        "formats": "CSV,JSON",
        "lastXDays": "7",
        "lastXDaysModified": "30",
    }
    assert get_search_params(input) == expected


@pytest.mark.unit
def test_search_param_validation_new_params_api() -> None:
    """Old API param names are mapped to canonical names"""
    input = {
        "q": "test query",
        "lostheme": "theme1,theme2",
        "theme": "AGRI,GOVE",
        "opendata": "true",
        "accessrights": "PUBLIC",
        "orgpath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
    }

    expected = {
        "query": "test query",
        "losTheme": "theme1,theme2",
        "dataTheme": "AGRI,GOVE",
        "openData": "true",
        "accessRights": "PUBLIC",
        "orgPath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
    }

    assert get_search_params(input) == expected
