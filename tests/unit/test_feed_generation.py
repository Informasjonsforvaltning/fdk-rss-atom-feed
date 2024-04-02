from typing import Any

from fdk_rss_atom_feed.feed import FeedType, generate_feed
import pytest


DATASETS_SEARCH_URL = (
    "https://search.api.staging.fellesdatakatalog.digdir.no/search/datasets"
)


@pytest.mark.unit
def test_rss_feed_generation(requests_mock: Any) -> None:
    with open("tests/test_data/mock_response0.json") as f:
        requests_mock.post(f"{DATASETS_SEARCH_URL}", text=f.read())

        feed = generate_feed(
            FeedType.RSS,
            args={
                "query": "testquery",
            },
        )

        decoded_feed = feed.decode("utf-8")
        print(decoded_feed)
        assert "7c5a0af9-e275-3d85-9871-5495f42530d8" in decoded_feed
        assert (
            "Dette er en test av å relatere til begrep i forbindelse med høsting av datasett_2702"
            in decoded_feed
        )

        assert "deead2b7-e50c-3285-9f38-807f8f816dac" in decoded_feed
        assert (
            "Test av relasjon mellom datasett og datasettserie via høsting"
            in decoded_feed
        )


@pytest.mark.unit
def test_atom_feed_generation(requests_mock: Any) -> None:
    with open("tests/test_data/mock_response0.json") as f:
        requests_mock.post(f"{DATASETS_SEARCH_URL}", text=f.read())

        feed = generate_feed(
            FeedType.ATOM,
            args={
                "query": "testquery",
            },
        )

        decoded_feed = feed.decode("utf-8")
        print(decoded_feed)
        assert "7c5a0af9-e275-3d85-9871-5495f42530d8" in decoded_feed
        assert (
            "Dette er en test av å relatere til begrep i forbindelse med høsting av datasett_2702"
            in decoded_feed
        )

        assert "deead2b7-e50c-3285-9f38-807f8f816dac" in decoded_feed
        assert (
            "Test av relasjon mellom datasett og datasettserie via høsting"
            in decoded_feed
        )
