from dataclasses import asdict
from enum import Enum
from json import JSONDecodeError
import logging
from typing import Any, Dict, List
from urllib.parse import urlencode

from fdk_rss_atom_feed.config import BASE_URL, DATASETS_SEARCH_URL
from fdk_rss_atom_feed.model import BadParamError, SearchOperation
from fdk_rss_atom_feed.query import construct_query
from fdk_rss_atom_feed.translation import translate_or_emptystr
from feedgen.feed import FeedEntry, FeedGenerator
import requests


ALL_AVAILABLE_SEARCH_PARAMETERS = (
    "q",
    "losTheme",
    "theme",
    "opendata",
    "accessrights",
    "orgPath",
    "spatial",
    "provenance",
    # Aligned with search-service:
    "query",
    "openData",
    "dataTheme",
    "accessRights",
)


SEARCH_SERVICE_PARAMS = (
    "query",
    "openData",
    "losTheme",
    "dataTheme",
    "accessRights",
    "orgPath",
    "spatial",
    "provenance",
)


param_map: Dict[str, str] = {
    "q": "query",
    "query": "query",
    "losTheme": "losTheme",
    "theme": "dataTheme",
    "dataTheme": "dataTheme",
    "opendata": "openData",
    "openData": "openData",
    "accessrights": "accessRights",
    "accessRights": "accessRights",
    "orgPath": "orgPath",
    "spatial": "spatial",
    "provenance": "provenance",
}


class FeedType(Enum):
    RSS = "rss"
    ATOM = "atom"


def generate_feed(feed_type: FeedType, args: Dict[str, str]) -> bytes:
    if len((invalid_params := invalid_search_params(args))) > 0:
        raise BadParamError(f"{', '.join(invalid_params)}")

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


def invalid_search_params(args: Dict[str, str]) -> List[str]:
    return [
        param for param in args.keys() if param not in ALL_AVAILABLE_SEARCH_PARAMETERS
    ]


def get_search_params(args: Dict[str, str]) -> Dict[str, str]:
    valid_input_params = {
        param_map[field]: args[field]
        for field in ALL_AVAILABLE_SEARCH_PARAMETERS
        if field in args
    }
    search_service_params = {
        key: value
        for key, value in valid_input_params.items()
        if key in SEARCH_SERVICE_PARAMS
    }
    return search_service_params


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

    if response.status_code != 200:
        logging.warning(
            f"Search request failed with status code {response.status_code}"
        )
        raise

    try:
        data = response.json()
    except JSONDecodeError as e:
        logging.warning(e.msg)
        logging.warning("Failed to decode search response")
        raise

    return data
