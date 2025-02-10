# Development Guide

## Heads-up!
Before starting development, ensure you:
- Create a virtual environment and activate it.
    - A good tool to manage virtualenvs is [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- Have a PostgreSQL instance running.
  - For Docker users, it is possible to create a postgres instance running `make run:db` in an individual terminal.
- Install dependencies using:
  ```sh
  pip install -r requirements.txt
  ```
  Alternatively, if you have [Poetry](https://python-poetry.org/) installed globally, you can use:
  ```sh
  poetry install
  ```
- Execute database migrations using:
  ```sh
  alembic upgrade head
  ```

For authentication, we are using fake users. You'll find (and register) users at:


```python
# src.config.fake_users_db

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

```

## Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- [pip](https://pip.pypa.io/en/stable/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [pytest](https://docs.pytest.org/en/stable/)
- [Ruff](https://github.com/charliermarsh/ruff)
- [isort](https://pycqa.github.io/isort/)

## Setup
1. Install dependencies:
   ```sh
   make install
   ```

## Running the Application
You can run the application in different environments using the following commands:

### Standard Run
```sh
make run
```
This starts the application using `fastapi run`.

### Development Mode
```sh
make run:dev
```
Runs the application in development mode using `fastapi dev`.

### Using Uvicorn
#### Production Mode
```sh
make run:uvi
```
Runs the application using `uvicorn` with `0.0.0.0` as the host.

#### Development Mode
```sh
make run:uvi:dev
```
Runs the application using `uvicorn` with auto-reloading enabled.

### Running with Docker
```sh
make run:docker
```
Runs the application inside a Docker container using `docker compose`.

## Database Setup
To start the PostgreSQL database:
```sh
make run:db
```

To apply migrations:
```sh
make migrate
```

## Linting & Formatting
To format and lint the code:
```sh
make lint
```
This runs `ruff format` and `isort` on the `src/` directory.

## Running Tests
To run tests with `pytest`:
```sh
make test
```
