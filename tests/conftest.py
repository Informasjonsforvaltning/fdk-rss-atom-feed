import os
import time
from typing import Any

import pytest
import requests
from requests.exceptions import ConnectionError


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> str:
    """Override default location of docker-compose.yml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yml")


@pytest.fixture(scope="session")
def elasticsearch_service(docker_ip: str, docker_services: Any) -> str:
    """Ensure that elasticsearch service is up and responsive."""
    port = docker_services.port_for("elasticsearch", 9200)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30, pause=0.1, check=lambda: is_ok(url)
    )
    return url


@pytest.fixture(scope="session")
def feed_service(docker_ip: str, docker_services: Any) -> str:
    """Ensure that feed service is up and responsive."""
    port = docker_services.port_for("fdk-rss-atom-feed", 8080)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30, pause=0.1, check=lambda: is_ok(url)
    )
    return url


@pytest.fixture(scope="session")
def elasticsearch_data(elasticsearch_service: str) -> None:
    """Ensure that elasticsearch service is up and has data."""
    for _ in range(120):
        response = requests.get(
            f"{elasticsearch_service}/datasets/_search",
            headers={"Content-Type": "application/json"},
            data='{"size": 0}',
        )
        if '"hits":{"total":{"value":100' in response.content.decode("utf-8"):
            return
        time.sleep(0.5)
    raise AssertionError(
        f"No datasets in index. status: {response.status_code} content: {response.content.decode('utf-8')}"
    )


@pytest.fixture(scope="session")
def elasticsearch_index(elasticsearch_service: str) -> dict:
    """Create elasticsearch datasets index."""
    requests.put(f"{elasticsearch_service}/datasets")
    return {}


def is_ok(url: str) -> bool:
    """Check if service returns 200 status."""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except ConnectionError:
        return False
