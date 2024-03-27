from enum import Enum
import logging
import os
from typing import Any, Dict, List
from urllib.parse import urlencode

from fdk_rss_atom_feed.model import SearchOperation
from fdk_rss_atom_feed.query import construct_query
from fdk_rss_atom_feed.translation import translate_or_emptystr
from feedgen.feed import FeedGenerator
from flask import abort
import requests


FDK_BASE_URI = os.getenv("FDK_BASE_URI", "https://staging.fellesdatakatalog.digdir.no")
BASE_URL = f"{FDK_BASE_URI}/datasets"

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


def generate_feed(feed_type: FeedType, args: Dict[str, str]) -> str:
    params = check_search_params(args)
    url = f"{BASE_URL}{url_encode(params)}"

    feed_generator = FeedGenerator()
    feed_generator.id(url)
    feed_generator.link(href=url)
    feed_generator.title("Felles datakatalog - Datasett")
    feed_generator.description("En samling av datasett publisert i Felles datakatalog")

    datasets = query_datasets(params.get("query", "").strip(), params)
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
    results = search(query, BASE_URL)
    hits = results["hits"]["hits"]
    return [hit["_source"] for hit in hits if "_source" in hit]


def check_search_params(args: Dict[str, str]) -> Dict[str, str]:
    valid_in_params = {
        param_map[field]: args[field]
        for field in ALL_AVAILABLE_SEARCH_PARAMETERS
        if field in args
    }
    search_service_params = {
        key: value
        for key, value in valid_in_params.items()
        if key in SEARCH_SERVICE_PARAMS
    }
    return search_service_params


def url_encode(params: Dict[str, str]) -> str:
    return f"?{urlencode(params)}" if len(params) > 0 else ""


def search(search_operation: SearchOperation, url: str) -> Dict[str, Any]:
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=search_operation.model_dump_json(),
            timeout=10,
        )
        response.raise_for_status()
    except ConnectionError:
        logging.warning("Connection error when fetching search results")
        abort(500)
    except requests.HTTPError as e:
        logging.warning(f"HTTP error when fetching search results: {e}")
        abort(500)
    except TimeoutError:
        logging.warning("Search request timed out")
        abort(500)

    if response.status_code != 200:
        logging.warning(
            f"Search request failed with status code {response.status_code}"
        )
        abort(500)

    return response.json()
