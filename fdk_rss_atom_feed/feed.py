from enum import Enum
import os
from typing import Dict, List
from urllib.parse import urlencode

from fdk_rss_atom_feed import es_client
from fdk_rss_atom_feed.query import construct_query
from fdk_rss_atom_feed.translation import translate_or_emptystr
from feedgen.feed import FeedGenerator


FDK_BASE_URI = os.getenv("FDK_BASE_URI", "https://staging.fellesdatakatalog.digdir.no")
BASE_URL = f"{FDK_BASE_URI}/datasets"

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


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def generate_feed(feed_type: FeedType, args: Dict[str, str]) -> str:
    params = search_params(args)
    url = f"{BASE_URL}{url_encode(params)}"

    feed_generator = FeedGenerator()
    feed_generator.id(url)
    feed_generator.link(href=url)
    feed_generator.title("Felles datakatalog - Datasett")
    feed_generator.description("En samling av datasett publisert i Felles datakataog")

    datasets = query_datasets(params.get("q", "").strip(), params)
    for dataset in datasets:
        feed_entry = feed_generator.add_entry()

        feed_entry.id(f"{BASE_URL}/{dataset['id']}")
        feed_entry.title(translate_or_emptystr(dataset["title"]))
        feed_entry.description(translate_or_emptystr(dataset["description"]))
        feed_entry.link(href=f"{BASE_URL}/{dataset['id']}")
        feed_entry.author(
            name=translate_or_emptystr(
                (dataset.get("publisher", {}) or {}).get("prefLabel", {})
                or (dataset.get("publisher", {}) or {}).get("name", {})
                or {}
            )
        )
        feed_entry.published(dataset["harvest"]["firstHarvested"])

    if feed_type == FeedType.RSS:
        return feed_generator.rss_str(pretty=True)
    elif feed_type == FeedType.ATOM:
        return feed_generator.atom_str(pretty=True)
    else:
        raise ValueError("Invalid feed type")


def query_datasets(q: str, params: Dict[str, str]) -> List[Dict]:
    query = construct_query(q, params)
    results = es_client.search(query)
    hits = results["hits"]["hits"]
    return [hit["_source"] for hit in hits if "_source" in hit]


def search_params(args: Dict[str, str]) -> Dict[str, str]:
    search_params = {
        field: args[field] for field in AVAILABLE_SEARCH_PARAMETERS if field in args
    }
    search_params["sortfield"] = "harvest.firstHarvested"
    return search_params


def url_encode(params: Dict[str, str]) -> str:
    return f"?{urlencode(params)}" if len(params) > 0 else ""
