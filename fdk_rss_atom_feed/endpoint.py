import logging
import traceback
from typing import Any

from fdk_rss_atom_feed.feed import FeedType, generate_feed
from flask import Request, Response
from flask_restful import abort


FEED_TYPES = {
    "application/rss+xml": FeedType.RSS,
    "application/atom+xml": FeedType.ATOM,
}


def feed(request: Request) -> Any:
    """Feed entrypoint"""
    mimetypes = ", ".join(FEED_TYPES.keys())
    supported_types = f"supported mime types: {{{mimetypes}}}\n"

    # If no mimetype is specified
    if request.accept_mimetypes.best == "*/*":
        return Response(supported_types)

    mimetype = request.accept_mimetypes.best
    try:
        feed_type = FEED_TYPES[mimetype]
    except KeyError:
        return abort(http_status_code=415, description=supported_types)

    try:
        feed = generate_feed(feed_type, dict(request.args.items()))
    except Exception:
        logging.error(
            f"{traceback.format_exc()}Error handling params: {str(list(request.args.items()))}"
        )
        return abort(http_status_code=500, description="Internal server error")

    return Response(feed, mimetype=mimetype)
