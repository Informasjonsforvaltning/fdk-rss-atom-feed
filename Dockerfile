FROM python:3.10

WORKDIR /app

RUN python3 -m pip install --no-cache-dir -q \
    poetry==1.1.13

COPY poetry.lock pyproject.toml ./
RUN python3 -m poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY fdk_rss_atom_feed fdk_rss_atom_feed
COPY app.py gunicorn_conf.py ./

EXPOSE 8080
CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:8080", "app:app"]
