from typing import Dict

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


def parse_filter_list(string: str | None) -> SearchFilter[list[str]] | None:
    if string is None:
        return None
    return SearchFilter(value=string.split(","))


def parse_boolean(string: str | None) -> SearchFilter[bool] | None:
    if string is None:
        return None
    return SearchFilter(value=(string.lower() == "true"))


def parse_string(string: str | None) -> SearchFilter[str] | None:
    if string is None:
        return None
    return SearchFilter(value=string)


def construct_query(search_string: str, params: Dict[str, str]) -> SearchOperation:
    return SearchOperation(
        query=search_string,
        filters=construct_filters(params),
        fields=Fields(title=True, description=True, keyword=True),
    )


def construct_filters(params: Dict[str, str]) -> Filters:
    return Filters(
        openData=parse_boolean(params.get("opendata", None)),
        orgPath=parse_string(params.get("orgPath", None)),
        accessRights=parse_string(params.get("accessrights", None)),
        dataTheme=parse_filter_list(params.get("theme", None)),
        losTheme=parse_filter_list(params.get("losTheme", None)),
        spatial=parse_filter_list(params.get("spatial", None)),
        provenance=parse_string(params.get("provenance", None)),
        formats=parse_filter_list(params.get("formats", None)),
        uri=None,
        lastXDays=None,
    )
