FROM python:3.10

WORKDIR /app

RUN python3 -m pip install --no-cache-dir -q \
    poetry==1.1.13

COPY poetry.lock pyproject.toml ./
# Flask is standin for gcloud's functions_framework in docker tests
RUN python3 -m poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && python3 -m pip install --no-cache-dir -q \
    flask==2.1.2 \
    Flask-RESTful==0.3.9

COPY fdk_rss_atom_feed fdk_rss_atom_feed
COPY app.py .

EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8000"]
