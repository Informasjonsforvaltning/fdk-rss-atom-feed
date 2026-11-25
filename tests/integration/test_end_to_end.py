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


@pytest.mark.integration
def test_list_filters_sent_as_lists(requests_mock: Any, flask_client: Any) -> None:
    with open("tests/test_data/mock_response0.json") as f:
        adapter = requests_mock.post(
            f"{SEARCH_SERVICE_BASE_URL}/search/datasets", text=f.read()
        )

    response = flask_client.get(
        "/?accessrights=PUBLIC,RESTRICTED&orgPath=/STAT/972417807&provenance=NASJONAL",
        headers={"Accept": "application/rss+xml"},
    )
    assert response.status_code == 200

    filters = adapter.last_request.json()["filters"]
    assert filters["accessRights"] == {"value": ["PUBLIC", "RESTRICTED"]}
    assert filters["orgPath"] == {"value": ["/STAT/972417807"]}
    assert filters["provenance"] == {"value": ["NASJONAL"]}


@pytest.mark.integration
@pytest.mark.parametrize("upstream_status", [400, 500, 503])
def test_search_service_error_returns_500(
    requests_mock: Any, flask_client: Any, upstream_status: int
) -> None:
    """An upstream 400 means the request contract has drifted, so it stays a 500"""
    requests_mock.post(
        f"{SEARCH_SERVICE_BASE_URL}/search/datasets", status_code=upstream_status
    )

    response = flask_client.get("/", headers={"Accept": "application/rss+xml"})
    assert response.status_code == 500


@pytest.mark.integration
@pytest.mark.parametrize("value", ["-1", "2147483648", "abc"])
def test_invalid_last_x_days_returns_400(
    requests_mock: Any, flask_client: Any, value: str
) -> None:
    adapter = requests_mock.post(f"{SEARCH_SERVICE_BASE_URL}/search/datasets")

    response = flask_client.get(
        f"/?lastXDays={value}", headers={"Accept": "application/rss+xml"}
    )
    assert response.status_code == 400
    assert not adapter.called
