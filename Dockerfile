FROM python:3.10-slim

WORKDIR /app

RUN python3 -m pip install --root-user-action=ignore --no-cache-dir -q \
    poetry==1.8.5

COPY poetry.lock pyproject.toml ./
RUN python3 -m poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY fdk_rss_atom_feed fdk_rss_atom_feed
COPY gunicorn_conf.py ./

EXPOSE 8080
CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:8080", "fdk_rss_atom_feed.app:app"]
