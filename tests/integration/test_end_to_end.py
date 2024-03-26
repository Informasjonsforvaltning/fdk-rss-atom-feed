import pytest
from tests.utils import get_feed, strip_dates


@pytest.mark.integration
def test_rss(feed_service: str) -> None:
    response = get_feed(f"{feed_service}?q=grunnkretser", "rss")
    assert response.status_code == 200
    with open("tests/data/rss_grunnkretser.xml", "r") as f:
        assert strip_dates(response.content.decode("utf-8")) == f.read()


@pytest.mark.integration
def test_atom(feed_service: str) -> None:
    response = get_feed(f"{feed_service}?q=siri", "atom")
    assert response.status_code == 200
    with open("tests/data/atom_siri.xml", "r") as f:
        assert strip_dates(response.content.decode("utf-8")) == f.read()
