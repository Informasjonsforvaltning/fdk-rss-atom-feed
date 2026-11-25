from typing import Dict, List

from fdk_rss_atom_feed.config import MAX_SEARCH_HITS
from fdk_rss_atom_feed.model import (
    BadParamError,
    Filters,
    Pagination,
    SearchFilter,
    SearchOperation,
    Sort,
)

MAX_INT = 2**31 - 1


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


def parse_int(string: str | None) -> SearchFilter[int] | None:
    if string is None:
        return None
    try:
        value = int(string)
    except ValueError as err:
        raise BadParamError(f"expected integer, got: {string!r}") from err
    # The search service deserializes this as a 32-bit Int and builds a
    # "now-<n>d" date range from it, so only 0..2^31-1 is meaningful.
    if not 0 <= value <= MAX_INT:
        raise BadParamError(f"expected integer in 0..{MAX_INT}, got: {string!r}")
    return SearchFilter[int](value=value)


def construct_query(search_string: str, params: Dict[str, str]) -> SearchOperation:
    return SearchOperation(
        query=search_string,
        filters=construct_filters(params),
        sort=Sort(field="FIRST_HARVESTED", direction="DESC"),
        pagination=Pagination(page=0, size=MAX_SEARCH_HITS),
    )


def construct_filters(params: Dict[str, str]) -> Filters:
    return Filters(
        openData=parse_boolean(params.get("openData", None)),
        orgPath=parse_filter_list(params.get("orgPath", None)),
        accessRights=parse_filter_list(params.get("accessRights", None)),
        dataTheme=parse_filter_list(params.get("dataTheme", None)),
        losTheme=parse_filter_list(params.get("losTheme", None)),
        spatial=parse_filter_list(params.get("spatial", None)),
        provenance=parse_filter_list(params.get("provenance", None)),
        formats=parse_filter_list(params.get("formats", None)),
        uri=None,
        lastXDays=parse_int(params.get("lastXDays", None)),
        lastXDaysModified=parse_int(params.get("lastXDaysModified", None)),
    )
