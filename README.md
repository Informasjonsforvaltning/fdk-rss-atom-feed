# fdk-rss-atom-feed

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
curl -H "Accept: application/rss+xml" localhost:8000
```

## Testing

```bash
nox
```

## Create `tests/data/datasets.json`

Run the following inside
[fdk-fulltext-search](https://github.com/Informasjonsforvaltning/fdk-fulltext-search):

```bash
docker-compose up -d
while ! curl -s localhost:9200 > /dev/null; do echo "startup..." && sleep 3; done
echo "index..."
curl -X POST -H "X-API-KEY: test-key" localhost:8000/indices?name=datasets
echo -e "\ndump..."
docker run --rm -it --net host -v $PWD:/mount elasticdump/elasticsearch-dump \
    elasticdump --input http://localhost:9200/datasets --output /mount/datasets_full.json
cat datasets_full.json | head -n 100 > datasets.json
rm -f datasets_full.json
docker-compose down
```
