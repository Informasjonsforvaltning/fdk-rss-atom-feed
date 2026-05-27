from dataclasses import asdict
from enum import Enum
from json import JSONDecodeError
import logging
from typing import Any, Dict, List
from urllib.parse import urlencode

from fdk_rss_atom_feed.config import BASE_URL, DATASETS_SEARCH_URL
from fdk_rss_atom_feed.model import SearchOperation
from fdk_rss_atom_feed.query import construct_query
from fdk_rss_atom_feed.translation import translate_or_emptystr
from feedgen.feed import FeedEntry, FeedGenerator
import requests

param_map: Dict[str, str] = {
    "q": "query",
    "query": "query",
    "lostheme": "losTheme",
    "theme": "dataTheme",
    "datatheme": "dataTheme",
    "opendata": "openData",
    "accessrights": "accessRights",
    "orgpath": "orgPath",
    "spatial": "spatial",
    "provenance": "provenance",
    "format": "formats",
    "formats": "formats",
    "lastxdays": "lastXDays",
    "lastxdaysmodified": "lastXDaysModified",
}


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def generate_feed(feed_type: FeedType, args: Dict[str, str]) -> bytes:
    args = {k.lower(): v for k, v in args.items()}
    params = get_search_params(args)
    url = f"{BASE_URL}{url_encode(params)}"

    feed_generator = FeedGenerator()
    feed_generator.id(url)
    feed_generator.link(href=url)
    feed_generator.title("Felles datakatalog - Datasett")
    feed_generator.description("En samling av datasett publisert i Felles datakatalog")

    datasets = query_datasets(params.get("query", "").strip(), params)
    for dataset in datasets:
        feed_entry = feed_generator.add_entry()
        populate_feed_entry(dataset, feed_entry)

    if feed_type == FeedType.RSS:
        return feed_generator.rss_str(pretty=True)
    elif feed_type == FeedType.ATOM:
        return feed_generator.atom_str(pretty=True)
    else:
        raise ValueError("Invalid feed type")


def populate_feed_entry(dataset: Dict[str, Any], feed_entry: FeedEntry) -> None:
    feed_entry.id(f"{BASE_URL}/{dataset['id']}")
    feed_entry.title(translate_or_emptystr(dataset.get("title", {})))
    feed_entry.description(translate_or_emptystr(dataset.get("description", {})))
    feed_entry.link(href=f"{BASE_URL}/{dataset['id']}")
    publisher: Dict = dataset.get("organization", {})
    publisher_name = (
        translate_or_emptystr(publisher.get("prefLabel", {}))
        or publisher.get("name")
        or publisher.get("uri")
        or ""
    )
    feed_entry.author(name=publisher_name)
    feed_entry.published(dataset.get("metadata", {}).get("firstHarvested", ""))


def query_datasets(q: str, params: Dict[str, str]) -> List[Dict]:
    query = construct_query(q, params)
    response = search(query, DATASETS_SEARCH_URL)
    try:
        hits: List[Dict] = response["hits"]
    except KeyError:
        logging.warning("Failed to get hits from search results")
        raise
    return hits


def get_search_params(args: Dict[str, str]) -> Dict[str, str]:
    return {param_map[field]: args[field] for field in param_map if field in args}


def url_encode(params: Dict[str, str]) -> str:
    return f"?{urlencode(params)}" if len(params) > 0 else ""


def search(search_operation: SearchOperation, url: str) -> Dict[str, Any]:
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            json=asdict(search_operation),
            timeout=10,
        )
        response.raise_for_status()
    except ConnectionError:
        logging.warning("Connection error when fetching search results")
        raise
    except requests.HTTPError as e:
        logging.warning(f"HTTP error when fetching search results: {e}")
        raise
    except TimeoutError:
        logging.warning("Search request timed out")
        raise

    try:
        data = response.json()
    except JSONDecodeError as e:
        logging.warning(e.msg)
        logging.warning("Failed to decode search response")
        raise

    return data
