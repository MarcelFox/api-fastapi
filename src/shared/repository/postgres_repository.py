from typing import List, Optional, TypeVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from src.shared.abstract.abstract_repository import AbstractRepository

T = TypeVar('T')

class PostgresRepository(AbstractRepository[T]):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.engine = create_async_engine(self.connection_url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def insert(self, entity) -> T | None:
        async with self.SessionLocal() as session:
            async with session.begin():
                session.add(entity)
                await session.flush()
                await session.refresh(entity)
                return entity
        return None

    async def find(self, entity: T, id: str) -> Optional[T]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(entity).filter(entity.id == id))
            return result.scalars().first()

    async def find_all(self) -> List[T]:
        async with self.SessionLocal() as session:
            result = await session.execute(select())
            return result.scalars().all()

    async def update(self, id: str, data: dict) -> T:
        async with self.SessionLocal() as session:
            async with session.begin():
                entity = await self.get(id)
                if entity:
                    for key, value in data.items():
                        setattr(entity, key, value)
                await session.commit()
                await session.refresh(entity)
                return entity

    async def delete(self, id: str) -> bool:
        async with self.SessionLocal() as session:
            async with session.begin():
                entity = await self.get(id)
                if not entity:
                    return False
                
                await session.delete(entity)
                await session.commit()
                return True

    async def execute(self, query: str) -> List[T] | T:
        async with self.SessionLocal() as session:
            async with session.begin():
                await session.execute(query)
