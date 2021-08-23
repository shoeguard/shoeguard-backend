# Shoeguard-Backend

## Technologies

- Python
  - Poetry
  - Django
  - Pytest
- Docker
  - Docker Compose
- PostgreSQL

## Install Required Packages

Run following commands to install poetry, an awesome package manager.

```sh
pip install poetry
```

and run following commands to install required packages

```sh
poetry install
```

Done!

## Running Tests

```sh
docker compose up --build test_db
pytest -vvk .
```

## Running server in debug mode

```sh
python3 manage.py runserver
```

## Running server in debug mode with docker

```sh
export DJANGO_SETTINGS_MODULE=shoeguard.configs.debug
docker compose up --build db was
```

## Running server in production mode with docker

First of all, you need to set your custom DJANGO_SECRET_KEY.

```sh
export DJANGO_SECRET_KEY = <the key you want>
```

```sh
export DJANGO_SETTINGS_MODULE=shoeguard.configs.prod
docker compose up --build db was
```
