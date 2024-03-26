from fdk_rss_atom_feed.feed import check_search_params
from fdk_rss_atom_feed.query import construct_query
import pytest


@pytest.mark.integration
def test_empty_query() -> None:
    """Assert empty query is correct."""
    assert construct_query("", {}) == {
        "query": {
            "bool": {
                "filter": [{"range": {"harvest.firstHarvested": {"gte": "now-1d/d"}}}],
                "must": [],
            }
        },
        "sort": {
            "harvest.firstHarvested": {
                "order": "desc",
                "unmapped_type": "long",
            }
        },
        "size": 1000,
    }


@pytest.mark.integration
def test_full_query() -> None:
    """Assert full query is correct."""
    params = check_search_params(
        {
            "opendata": "true",
            "theme": "EDUC",
            "spatial": "Oslo",
            "orgPath": "/STAT/972417920/971277882",
            "accessrights": "PUBLIC",
            "losTheme": "trafikk-og-transport,veg-og-vegregulering",
            "provenance": "MISSING",
            "other": "field",
        }
    )
    query = construct_query("foo :/ bar", params)
    assert query["query"] == {
        "bool": {
            "must": [
                {
                    "dis_max": {
                        "queries": [
                            {
                                "multi_match": {
                                    "query": "foo :/ bar",
                                    "type": "bool_prefix",
                                    "fields": [
                                        "title.en.ngrams",
                                        "title.en.ngrams.2_gram",
                                        "title.en.ngrams.3_gram",
                                        "title.nb.ngrams",
                                        "title.nb.ngrams.2_gram",
                                        "title.nb.ngrams.3_gram",
                                        "title.nn.ngrams",
                                        "title.nn.ngrams.2_gram",
                                        "title.nn.ngrams.3_gram",
                                        "title.no.ngrams",
                                        "title.no.ngrams.2_gram",
                                        "title.no.ngrams.3_gram",
                                    ],
                                }
                            },
                            {
                                "multi_match": {
                                    "query": "foo :/ bar",
                                    "fields": [
                                        "title.en.raw",
                                        "title.nb.raw",
                                        "title.nn.raw",
                                        "title.no.raw",
                                        "publisher.prefLabel.*",
                                        "publisher.title.*",
                                        "hasCompetentAuthority.prefLabel.*",
                                        "hasCompetentAuthority.name.*",
                                        "keyword.*",
                                    ],
                                }
                            },
                            {
                                "simple_query_string": {
                                    "query": "foo+:/+bar foo+:/+bar*",
                                    "fields": [
                                        "description.en",
                                        "description.nb",
                                        "description.nn",
                                        "description.no",
                                    ],
                                }
                            },
                            {
                                "simple_query_string": {
                                    "query": "foo+bar foo+bar*",
                                    "fields": [
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
                                    ],
                                }
                            },
                            {
                                "query_string": {
                                    "query": "*foo* *bar*",
                                    "fields": [
                                        "title.en.raw",
                                        "title.nb.raw",
                                        "title.nn.raw",
                                        "title.no.raw",
                                    ],
                                }
                            },
                        ]
                    }
                }
            ],
            "filter": [
                {"term": {"publisher.orgPath": "/STAT/972417920/971277882"}},
                {"term": {"accessRights.code.keyword": "PUBLIC"}},
                {"term": {"losTheme.losPaths.keyword": "trafikk-og-transport"}},
                {"term": {"losTheme.losPaths.keyword": "veg-og-vegregulering"}},
                {"term": {"euTheme": "EDUC"}},
                {
                    "bool": {
                        "must_not": {"exists": {"field": "provenance.code.keyword"}}
                    }
                },
                {"term": {"spatial.prefLabel.no.keyword": "Oslo"}},
                {"term": {"accessRights.code.keyword": "PUBLIC"}},
                {"term": {"isOpenData": "true"}},
                {"range": {"harvest.firstHarvested": {"gte": "now-1d/d"}}},
            ],
        }
    }
