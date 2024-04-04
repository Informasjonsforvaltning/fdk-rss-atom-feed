import os


FDK_BASE_URI = os.getenv("FDK_BASE_URI", "https://staging.fellesdatakatalog.digdir.no")
BASE_URL = f"{FDK_BASE_URI}/datasets"

SEARCH_API = os.getenv(
    "SEARCH_API", "https://search.api.staging.fellesdatakatalog.digdir.no"
)
DATASETS_SEARCH_URL = f"{SEARCH_API}/search/datasets"

MAX_SEARCH_HITS = 10_000
