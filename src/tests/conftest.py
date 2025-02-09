"""Test configuration module."""

import asyncio
import hashlib
import os
import secrets
from typing import Any, AsyncGenerator

import psycopg2
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

TEST_DATABASE_NAME = "test_db"
ADMIN_DATABASE_URL = "postgresql://user:password@localhost/postgres"
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/test_db"

try:
    conn = psycopg2.connect(ADMIN_DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DATABASE_NAME,)
    )
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {TEST_DATABASE_NAME}")
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
    conn.close()
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists.")
except psycopg2.errors.UniqueViolation as err:
    print(err)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_test_db():
    yield  # Wait until all tests are done

    await drop_database()


async def drop_database():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _drop_database_sync)


def _drop_database_sync():
    try:
        connection = psycopg2.connect(ADMIN_DATABASE_URL)
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME};")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error dropping database: {e}")


@pytest_asyncio.fixture
async def random_hash() -> str:
    random_string = secrets.token_hex(16)
    hash_object = hashlib.sha256(random_string.encode())
    return hash_object.hexdigest()


@pytest_asyncio.fixture
async def headers() -> dict:
    return {
        "Content-Type": "application/json",
        "User-Agent": "insomnium/0.2.3-a",
        "Authorization": "Bearer johndoe",
    }


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[Any, Any]:
    os.environ["POSTGRES_URL"] = TEST_DATABASE_URL
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://0.0.0.0"
    ) as test_client:
        yield test_client
