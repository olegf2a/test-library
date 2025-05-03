## Setup project

### 1. Clone code from a repository to local folder

```bash
git clone <repo-url>

cd your_project_name
```

### 2.1 Run using Docker (Postgres + FastAPI)

* Setup application with database:

```bash
docker-compose up -d
```
* Once the application is up, the OpenAPI docs are available at

```bash
 http://0.0.0.0:8008/api/docs
```

### 2.2 Run locally (Postgres in container, FastAPI locally)

* Open [docker-compose.yml](docker-compose.yml) file and comment `fastapi` section

* Create virtual environment using python 3.12 and activate (optional):

```bash
 python3.12 -m venv venv

 source venv/bin/activate
```

*  Install dependencies:

```bash
 cd your_project_name

 poetry install --with dev
```

* Start the database:

```bash
docker-compose up -d
```

* Apply migrations:

```bash
alembic upgrade head
```

* Run tests:

```bash
pytest
```

* Run the application:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8008
```

* Open API docs:

```bash
 http://0.0.0.0:8008/api/docs
```

## Activate pre-commit

[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black or its nowadays replacement ruff.

Refer to `.pre-commit-config.yaml` file to see my current opinionated choices.

```bash
# Install pre-commit
pre-commit install --install-hooks

# Run on all files
pre-commit run --all-files
```
