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
curl -H "Accept: application/rss+xml" localhost:8000
```

Kibana's dev tools console may be helpful when developing:

```bash
docker run --rm -it --network host -e ELASTICSEARCH_HOSTS='["http://localhost:9200"]' kibana:8.10.4
```

Then create queries such as the one below in <http://localhost:5601/app/dev_tools#/console>.

```json
GET datasets/_search
{
  "query": {
    "match_all": {}
  },
  "size": 100,
  "sort": {
    "harvest.firstHarvested": {
      "order": "desc",
      "unmapped_type": "long"
    }
  }
}
```

## Testing

[nox](https://nox.thea.codes/en/stable/) is used for testing:

```bash
nox
```

### Datasets

The content of `tests/data/datasets.json` is used for testing, and is loaded into elasticsearch.
To recreate such a file, run the following inside
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
