from fdk_rss_atom_feed.feed import get_search_params, invalid_search_params
import pytest


@pytest.mark.unit
def test_search_param_validation() -> None:
    """All fields valid, should return the same dict"""
    input = {
        "query": "test query",
        "losTheme": "theme1,theme2",
        "dataTheme": "AGRI,GOVE",
        "openData": "true",
        "accessRights": "PUBLIC",
        "orgPath": "987654321",
        "spatial": "Oslo",
        "provenance": "PROVENANCE",
    }

    expected = input.copy()
    assert get_search_params(input) == expected


@pytest.mark.unit
def test_search_param_validation_with_invalid_params() -> None:
    """Some params invalid, should ignore them"""
    input = {
        "q": "test query",
        "losTheme": "theme1,theme2",
        "invalidParam": "something",
        "anotherInvalidParam": "something2",
    }

    assert get_search_params(input).get("invalidParam", None) is None
    assert get_search_params(input).get("anotherInvalidParam", None) is None


@pytest.mark.unit
def test_search_param_validation_new_params_api() -> None:
    """All fields valid on old API, should return correct mapping"""
    input = {
        "q": "test query",
        "losTheme": "theme1,theme2",
        "theme": "AGRI,GOVE",
        "opendata": "true",
        "accessrights": "PUBLIC",
        "orgPath": "987654321",
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


@pytest.mark.unit
def test_catch_invalid_search_params() -> None:
    """Should return list of invalid params"""
    input = {
        "q": "test query",
        "invalidParam": "x",
        "anotherInvalidParam": "x",
        "opendata": "true",
        "lastInvalidParam": "x",
        "orgPath": "987654321",
    }

    expected = ["invalidParam", "anotherInvalidParam", "lastInvalidParam"]

    assert invalid_search_params(input) == expected
