from fdk_rss_atom_feed.endpoint import feed
from flask import Request
import functions_framework


@functions_framework.http
def main(request: Request) -> str:
    """Cloud function"""

    return feed(request)
