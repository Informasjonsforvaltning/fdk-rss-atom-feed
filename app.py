from fdk_rss_atom_feed.endpoint import feed
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def main() -> str:
    """Flask development function"""

    return feed(request)
