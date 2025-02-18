import logging
import traceback
from typing import Any

from fdk_rss_atom_feed.feed import FeedType, generate_feed, SEARCH_SERVICE_PARAMS
from fdk_rss_atom_feed.model import BadParamError
from flask import abort, Request, Response


FEED_TYPES = {
    "application/rss+xml": FeedType.RSS,
    "application/atom+xml": FeedType.ATOM,
}


def feed(request: Request) -> Any:
    """Feed entrypoint"""

    mimetype = request.accept_mimetypes.best

    if mimetype not in FEED_TYPES.keys():
        mimetypes = ", ".join(FEED_TYPES.keys())
        supported_types = (
            "The server does not support the media type transmitted in the request."
            + f" Supported media types are: {{{mimetypes}}}."
        )
        return abort(415, supported_types)
    else:
        feed_type = FEED_TYPES[mimetype]

    try:
        feed = generate_feed(feed_type, dict(request.args.items()))
    except BadParamError as e:
        return abort(
            400,
            f"Invalid search param(s): {e}. "
            f"Supported params: {', '.join(SEARCH_SERVICE_PARAMS)}",
        )

    except Exception:
        logging.error(
            f"{traceback.format_exc()}Error handling params: {str(list(request.args.items()))}"
        )
        return abort(500)

    return Response(feed, mimetype=mimetype)
