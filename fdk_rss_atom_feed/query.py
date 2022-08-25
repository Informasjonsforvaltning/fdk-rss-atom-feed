import re
from typing import Any, Dict, List

ABSENT_FIELD_VALUES = ("MISSING", "Ukjent")
LANGUAGES = ("en", "nb", "nn", "no")
NGRAM_POSTFIXES = ("", ".2_gram", ".3_gram")

PARAM_SEARCH_FIELDS = {
    "orgPath": "publisher.orgPath",
    "accessrights": "accessRights.code.keyword",
    "losTheme": "losTheme.losPaths.keyword",
    "theme": "euTheme",
    "provenance": "provenance.code.keyword",
    "spatial": "spatial.prefLabel.no.keyword",
}

FULLTEXT_FIELDS = (
    "accessRights.code",
    "accessRights.prefLabel.*",
    "description.*",
    "distribution.format",
    "distribution.title.*",
    "keyword.*",
    "losTheme.name.*",
    "objective.*",
    "publisher.name",
    "publisher.prefLabel",
    "subject.altLabel.*",
    "subject.definition.*",
    "subject.prefLabel.*",
    "theme.title.*",
    "title.*",
)
OPENDATA_FILTERS = {
    "accessRights.code.keyword": "PUBLIC",
    "isOpenData": "true",
}
ORGANIZATION_AND_KEYWORDS = (
    "publisher.prefLabel.*",
    "publisher.title.*",
    "hasCompetentAuthority.prefLabel.*",
    "hasCompetentAuthority.name.*",
    "keyword.*",
)


def construct_query(search_string: str, params: Dict[str, str]) -> dict[str, Any]:
    return {
        "query": {
            "bool": {
                "must": construct_must_queries(search_string),
                "filter": [
                    *construct_filters(params),
                    last_days_range(1),
                ],
            },
        },
        "sort": {
            "harvest.firstHarvested": {
                "order": "desc",
                "unmapped_type": "long",
            }
        },
        "size": 1000,
    }


def last_days_range(n: int) -> dict[str, dict[str, dict[str, str]]]:
    return {
        "range": {
            "harvest.firstHarvested": {
                "gte": f"now-{n}d/d",
            },
        },
    }


def construct_filters(params: dict[str, str]) -> List[dict]:
    filters: List[dict[str, Any]] = []

    for param_key, search_field in PARAM_SEARCH_FIELDS.items():
        if param_key in params:
            param_value = params[param_key]

            if param_value in ABSENT_FIELD_VALUES:
                filters.append(
                    {"bool": {"must_not": {"exists": {"field": search_field}}}}
                )
            else:
                for term in param_value.split(","):
                    filters.append(
                        {
                            "term": {
                                search_field: term,
                            },
                        }
                    )

    if "opendata" in params:
        for key, value in OPENDATA_FILTERS.items():
            filters.append({"term": {key: value}})

    return filters


def construct_must_queries(search_string: str) -> List[dict[str, Any]]:
    if not search_string:
        return []

    words = re.findall(r"\w+", search_string)
    plus_delimited = search_string.replace(" ", "+")
    plus_delimited_words = "+".join(words) or plus_delimited

    queries = [
        {
            "multi_match": {  # Non-exact match on title
                "query": search_string,
                "type": "bool_prefix",
                "fields": [
                    f"title.{lang}.ngrams{postfix}"
                    for lang in LANGUAGES
                    for postfix in NGRAM_POSTFIXES
                ],
            }
        },
        {
            "multi_match": {
                "query": search_string,
                "fields": [
                    *[
                        f"title.{lang}.raw" for lang in LANGUAGES
                    ],  # Exact match on title
                    *ORGANIZATION_AND_KEYWORDS,  # Organization and keywords
                ],
            }
        },
        {
            "simple_query_string": {  # Description
                "query": f"{plus_delimited} {plus_delimited}*",
                "fields": [f"description.{lang}" for lang in LANGUAGES],
            }
        },
        {
            "simple_query_string": {  # Fulltext fields
                "query": f"{plus_delimited_words} {plus_delimited_words}*",
                "fields": list(FULLTEXT_FIELDS),
            }
        },
    ]

    if words:
        queries.append(
            {
                "query_string": {  # Non-exact match on title
                    "query": " ".join([f"*{word}*" for word in words]),
                    "fields": [f"title.{lang}.raw" for lang in LANGUAGES],
                }
            }
        )

    return [{"dis_max": {"queries": queries}}]
