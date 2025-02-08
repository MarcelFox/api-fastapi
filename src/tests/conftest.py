"""Test configuration module."""

import hashlib
import secrets
from typing import Any, AsyncGenerator

import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from src.main import app
from src.shared.classes.declarative_base import Base


@pytest_asyncio.fixture
def random_hash() -> str:
    random_string = secrets.token_hex(16)
    hash_object = hashlib.sha256(random_string.encode())
    return hash_object.hexdigest()

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_and_teardown():
    async_engine = create_async_engine("postgresql+asyncpg://user:password@0.0.0.0/test_db", echo=True)

    if not database_exists:
        create_database(async_engine.url)
        run_migrations()

    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
    async with async_session() as db:
        yield db

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture
async def client(setup_and_teardown) -> AsyncGenerator[Any, Any]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://0.0.0.0") as test_client:
        yield test_client
