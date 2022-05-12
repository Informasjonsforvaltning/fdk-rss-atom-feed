import re
from typing import Any

import requests


def get_feed(url: str, mimetype: str) -> Any:
    """Request feed in specific format."""
    headers = {"Accept": f"application/{mimetype}+xml"}
    return requests.get(url, headers=headers)


def strip_dates(content: str) -> str:
    """Strip dates in rss/atom feed."""
    content = re.sub("\n +<lastBuildDate>.*</lastBuildDate>\n", "\n", content)
    content = re.sub("\n +<updated>.*</updated>\n", "\n", content)
    return content


def strip_entries(content: str) -> str:
    """Strip all dataset entries in rss/atom feed."""
    content = re.sub("\n +<entry>.*</entry>\n", "\n", content, flags=re.DOTALL)
    content = re.sub("\n +<item>.*</item>\n", "\n", content, flags=re.DOTALL)
    return content
