import pytest
import requests


@pytest.mark.contract
def test_readyz(feed_service: str) -> None:
    response = requests.get(f"{feed_service}/readyz")
    assert response.status_code == 200


@pytest.mark.contract
def test_livez(feed_service: str) -> None:
    response = requests.get(f"{feed_service}/livez")
    assert response.status_code == 200
