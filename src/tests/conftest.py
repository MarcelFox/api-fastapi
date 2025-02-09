"""Test configuration module."""

import asyncio
import hashlib
import os
import secrets
from typing import Any, AsyncGenerator
import asyncpg
import pytest
import pytest_asyncio
from alembic.config import Config
from alembic import command
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from src.shared.classes.declarative_base import Base

@pytest_asyncio.fixture(scope='session')
def startup_and_teardown():
    print('\n\nSTART SETUP FOR TESTS')
    # os.environ["POSTGRES_URL"] = "postgresql+asyncpg://user:password@0.0.0.0/test_db"
    yield
    print('\nRUNNING TEARDOWN')

@pytest_asyncio.fixture
def random_hash() -> str:
    random_string = secrets.token_hex(16)
    hash_object = hashlib.sha256(random_string.encode())
    return hash_object.hexdigest()

@pytest_asyncio.fixture
async def client(startup_and_teardown) -> AsyncGenerator[Any, Any]:
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app), base_url="http://0.0.0.0") as test_client:
        yield test_client
