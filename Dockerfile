FROM python:3.12-slim AS builder

WORKDIR /app

RUN python3 -m pip install --root-user-action=ignore --no-cache-dir -q \
    poetry==2.5.1 \
    && poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root --no-interaction --no-ansi

FROM python:3.12-slim

WORKDIR /app

# Patch OS packages (perl-base, openssl, gzip, glibc, pcre2, sqlite, …)
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY fdk_rss_atom_feed fdk_rss_atom_feed

EXPOSE 8080
CMD ["gunicorn", "--config=fdk_rss_atom_feed/gunicorn_conf.py", "--bind", "0.0.0.0:8080", "fdk_rss_atom_feed.app:app"]
