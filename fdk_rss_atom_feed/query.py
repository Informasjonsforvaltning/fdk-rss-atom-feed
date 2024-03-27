from typing import Dict, List

from fdk_rss_atom_feed.model import (
    Fields,
    Filters,
    SearchFilter,
    SearchOperation,
)


def parse_filter_list(
    string: str | None,
) -> SearchFilter[List[str]] | None:
    if string is None:
        return None
    return SearchFilter[List[str]](value=string.split(","))


def parse_boolean(string: str | None) -> SearchFilter[bool] | None:
    if string is None:
        return None
    return SearchFilter[bool](value=(string.lower() == "true"))


def parse_string(string: str | None) -> SearchFilter[str] | None:
    if string is None:
        return None
    return SearchFilter[str](value=string)


def construct_query(search_string: str, params: Dict[str, str]) -> SearchOperation:
    return SearchOperation(
        query=search_string,
        filters=construct_filters(params),
        fields=Fields(title=True, description=True, keyword=True),
    )


def construct_filters(params: Dict[str, str]) -> Filters:
    return Filters(
        openData=parse_boolean(params.get("openData", None)),
        orgPath=parse_string(params.get("orgPath", None)),
        accessRights=parse_string(params.get("accessRights", None)),
        dataTheme=parse_filter_list(params.get("dataTheme", None)),
        losTheme=parse_filter_list(params.get("losTheme", None)),
        spatial=parse_filter_list(params.get("spatial", None)),
        provenance=parse_string(params.get("provenance", None)),
        formats=parse_filter_list(params.get("formats", None)),
        uri=None,
        lastXDays=None,
    )
