# fdk-rss-atom-feed

An RSS/atom feed that returns datasets harvested the previous 24h.
The service may be queried with specific parameters to limit the results.

## Development

### Requirements

- [docker compose](https://docs.docker.com/compose/)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Installation

```bash
pip install docker-compose nox nox-poetry poetry
poetry install
```

### Running locally

```bash
docker-compose up -d
```

You may then query the service:

```bash
curl -H "Accept: application/rss+xml" localhost:8080
```

```bash
curl -H "Accept: application/atom+xml" localhost:8080
```

## Testing

[nox](https://nox.thea.codes/en/stable/) is used for testing:

```bash
nox
```
