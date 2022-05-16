import logging
import traceback
from typing import Any

from fdk_rss_atom_feed import es_client
from fdk_rss_atom_feed.feed import FeedType, generate_feed
from flask import abort, Request, Response


FEED_TYPES = {
    "application/rss+xml": FeedType.RSS,
    "application/atom+xml": FeedType.ATOM,
}


def feed(request: Request) -> Any:
    """Feed entrypoint"""

    mimetype = request.accept_mimetypes.best
    try:
        feed_type = FEED_TYPES[mimetype]
    except KeyError:
        mimetypes = ", ".join(FEED_TYPES.keys())
        supported_types = (
            "The server does not support the media type transmitted in the request."
            + f" Supported media types are: {{{mimetypes}}}."
        )
        return abort(415, supported_types)

    try:
        feed = generate_feed(feed_type, dict(request.args.items()))
    except Exception:
        logging.error(
            f"{traceback.format_exc()}Error handling params: {str(list(request.args.items()))}"
        )
        return abort(500)

    return Response(feed, mimetype=mimetype)


def test_connection(_: Request) -> Any:
    """Test elasticsearch connection"""
    try:
        result = es_client.search({"size": 0})
        if not result["_shards"]["total"] == result["_shards"]["successful"]:
            logging.warning(f"Elasticsearch query not successful: {str(result)}")
    except IndexError:
        logging.error(f"{traceback.format_exc()}Error checking elasticsearch result")
        return abort(500)
    except Exception:
        logging.error(f"{traceback.format_exc()}Error connecting to elasticsearch")
        return abort(500)

    return Response("ok")
