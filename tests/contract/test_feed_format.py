import pytest
import requests
from tests.utils import get_feed, strip_dates, strip_entries


@pytest.mark.contract
def test_rss(feed_service: str, elasticsearch_index: str) -> None:
    response = get_feed(feed_service, "rss")
    assert response.status_code == 200
    empty_feed = strip_entries(response.content.decode("utf-8"))
    assert "<lastBuildDate>" in empty_feed
    assert "</lastBuildDate>" in empty_feed
    with open("tests/data/rss.xml", "r") as f:
        assert strip_dates(empty_feed) == f.read()


@pytest.mark.contract
def test_atom(feed_service: str, elasticsearch_index: str) -> None:
    response = get_feed(feed_service, "atom")
    assert response.status_code == 200
    empty_feed = strip_entries(response.content.decode("utf-8"))
    assert "<updated>" in empty_feed
    assert "</updated>" in empty_feed
    with open("tests/data/atom.xml", "r") as f:
        assert strip_dates(empty_feed) == f.read()


@pytest.mark.contract
def test_readyz(feed_service: str, elasticsearch_index: str) -> None:
    response = requests.get(f"{feed_service}/readyz")
    assert response.status_code == 200


@pytest.mark.contract
def test_livez(feed_service: str, elasticsearch_index: str) -> None:
    response = requests.get(f"{feed_service}/livez")
    assert response.status_code == 200
