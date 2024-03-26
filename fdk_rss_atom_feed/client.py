import os
from typing import Any

# from elastic_transport import ObjectApiResponse
# from elasticsearch import Elasticsearch


# class Client:
#     def __init__(self) -> None:
#         host = os.getenv("ELASTIC_HOST", "http://localhost")
#         port = os.getenv("ELASTIC_PORT", "9200")
#         self.es = Elasticsearch([f"{host}:{port}"])

#     def search(self, query: dict[str, Any]) -> ObjectApiResponse[Any]:
#         return self.es.search(index="datasets", **query)
