from fdk_rss_atom_feed.endpoint import feed
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def main() -> str:
    """Main endpoint"""
    return feed(request)


@app.route("/livez")
def livez() -> str:
    """Liveness endpoint"""
    return "ok"


@app.route("/readyz")
def readyz() -> str:
    """Readiness endpoint"""
    return "ok"
