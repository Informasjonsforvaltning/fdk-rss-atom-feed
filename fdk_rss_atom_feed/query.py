from typing import Any, Dict, List

from fdk_rss_atom_feed.model import Fields, Filters, SearchFilter, SearchOperation


AVAILABLE_QUERY_PARAMS = (
    "query",
    "description",
    "keyword",
)
AVAILABLE_SEARCH_PARAMETERS = (
    "q",
    "losTheme",
    "theme",
    "opendata",
    "accessrights",
    "orgPath",
    "spatial",
    "provenance",
)


def parse_filter_list(string: str | None) -> list[str] | None:
    if string is None:
        return None
    return string.split(",")


def parse_boolean(string: str | None) -> bool | None:
    if string is None:
        return None
    return string.lower() == "true"


def parse_string(string: str | None) -> str | None:
    if string is None:
        return None
    return string


def construct_query(search_string: str, params: Dict[str, str]) -> SearchOperation:
    return SearchOperation(
        query=search_string,
        filters=construct_filters(params),
        fields=Fields(title=True, description=True, keyword=True),
    )


def construct_filters(params: Dict[str, str]) -> Filters:
    return Filters(
        openData=SearchFilter(parse_boolean(params.get("opendata", None))),
        orgPath=SearchFilter(parse_string(params.get("orgPath", None))),
        accessRights=SearchFilter(parse_string(params.get("accessrights", None))),
        dataTheme=SearchFilter(parse_filter_list(params.get("theme", None))),
        losTheme=SearchFilter(parse_filter_list(params.get("losTheme", None))),
        spatial=SearchFilter(parse_filter_list(params.get("spatial", None))),
        provenance=SearchFilter(parse_string(params.get("provenance", None))),
        formats=SearchFilter(parse_filter_list(params.get("formats", None))),
        uri=None,
        lastXDays=SearchFilter(value=1),
    )


def search(searchOperation: SearchOperation) -> Dict[str, Any]:
    return dict()
