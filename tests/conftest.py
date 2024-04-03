import os
from typing import Any

from fdk_rss_atom_feed.app import app as flask_app
import pytest
import requests
from requests.exceptions import ConnectionError


SEARCH_SERVICE_BASE_URL = os.getenv(
    "SEARCH_SERVICE_URL",
    "https://search.api.staging.fellesdatakatalog.digdir.no",
)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> str:
    """Override default location of docker-compose.yml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yml")


@pytest.fixture(scope="session")
def feed_service(docker_ip: str, docker_services: Any) -> str:
    """Ensure that feed service is up and responsive."""
    port = docker_services.port_for("fdk-rss-atom-feed", 8080)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30, pause=0.1, check=lambda: is_ok(url, 415)
    )
    return url


def is_ok(url: str, code: int = 200) -> bool:
    """Check if service returns correct status."""
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == code
    except ConnectionError:
        return False


@pytest.fixture()
def app():
    app = flask_app
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def flask_client(app):
    return app.test_client()


@pytest.fixture()
def flask_runner(app):
    return app.test_cli_runner()
