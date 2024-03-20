import logging
import os
from typing import Any

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch


class Client:
    def __init__(self) -> None:
        elastic_host = os.getenv("ELASTIC_HOST", "http://localhost:9200")
        elastic_user = os.getenv("ELASTIC_USER", "")
        elastic_pwd = os.getenv("ELASTIC_PASSWORD", "")
        elastic_ca_cert = os.getenv("ELASTIC_CA_CERT", None)

        if elastic_ca_cert is None:
            logging.warning(
                "No ELASTIC_CA_CERT environment variable set. "
                "This is only safe for development and testing."
            )
            self.es = Elasticsearch(
                hosts=[f"{elastic_host}"],
                basic_auth=(elastic_user, elastic_pwd),
            )
        else:
            logging.warning("Found certificate")
            try:
                self.es = Elasticsearch(
                    hosts=[f"{elastic_host}"],
                    basic_auth=(elastic_user, elastic_pwd),
                    verify_certs=True,
                    ca_certs=f"{elastic_ca_cert}",
                )
            except Exception as e:
                logging.error(f"Failed to connect to Elasticsearch: {e}")
                raise

    def search(self, query: dict[str, Any]) -> ObjectApiResponse[Any]:
        return self.es.search(index="datasets", **query)
