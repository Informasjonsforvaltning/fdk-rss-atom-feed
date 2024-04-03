from typing import Any

import pytest
from tests.conftest import SEARCH_SERVICE_BASE_URL


@pytest.mark.integration
def test_rss(requests_mock: Any, flask_client: Any) -> None:
    with open("tests/test_data/mock_response0.json") as f:
        requests_mock.post(f"{SEARCH_SERVICE_BASE_URL}/search/datasets", text=f.read())

        response = flask_client.get("/", headers={"Accept": "application/rss+xml"})
        assert response.status_code == 200
        feed = response.text

        assert "7c5a0af9-e275-3d85-9871-5495f42530d8" in feed
        assert (
            "Dette er en test av å relatere til begrep i forbindelse med høsting av datasett_2702"
            in feed
        )

        assert "deead2b7-e50c-3285-9f38-807f8f816dac" in feed
        assert "Test av relasjon mellom datasett og datasettserie via høsting" in feed


@pytest.mark.integration
def test_atom(requests_mock: Any, flask_client: Any) -> None:
    with open("tests/test_data/mock_response0.json") as f:
        requests_mock.post(f"{SEARCH_SERVICE_BASE_URL}/search/datasets", text=f.read())

        response = flask_client.get("/", headers={"Accept": "application/atom+xml"})
        assert response.status_code == 200
        feed = response.text

        assert "7c5a0af9-e275-3d85-9871-5495f42530d8" in feed
        assert (
            "Dette er en test av å relatere til begrep i forbindelse med høsting av datasett_2702"
            in feed
        )

        assert "deead2b7-e50c-3285-9f38-807f8f816dac" in feed
        assert "Test av relasjon mellom datasett og datasettserie via høsting" in feed
