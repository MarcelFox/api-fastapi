"""Test configuration module."""

import asyncio
import hashlib
import os
import secrets
from typing import Any, AsyncGenerator
import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from src.shared.classes.declarative_base import Base
import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import psycopg2

# @pytest.fixture(scope="session")
# def event_loop():
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

ADMIN_DATABASE_URL = "postgresql://user:password@0.0.0.0/postgres"
TEST_DATABASE_NAME = "test_db"

@pytest_asyncio.fixture(scope='session', autouse=True)
async def startup():
    print('\n\nSTART SETUP FOR TESTS')
    try:
        conn = psycopg2.connect(ADMIN_DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DATABASE_NAME,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {TEST_DATABASE_NAME}')
            alembic_cfg = Config("alembic.ini")
            await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists.")

@pytest_asyncio.fixture
async def random_hash() -> str:
    random_string = secrets.token_hex(16)
    hash_object = hashlib.sha256(random_string.encode())
    return hash_object.hexdigest()

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[Any, Any]:
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app), base_url="http://0.0.0.0") as test_client:
        yield test_client
