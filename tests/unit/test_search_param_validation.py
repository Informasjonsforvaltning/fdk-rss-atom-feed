from fdk_rss_atom_feed.feed import check_search_params
import pytest


@pytest.mark.unit
def test_search_param_validation() -> None:
    """All fields valid, should return the same dict"""
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

    expected = input.copy()
    assert check_search_params(input) == expected


@pytest.mark.unit
def test_search_param_validation_with_invalid_params() -> None:
    """Some params invalid, should ignore them"""
    input = {
        "q": "test query",
        "losTheme": "theme1,theme2",
        "invalidParam": "something",
        "anotherInvalidParam": "something2",
    }

    assert check_search_params(input).get("invalidParam", None) is None
    assert check_search_params(input).get("anotherInvalidParam", None) is None
