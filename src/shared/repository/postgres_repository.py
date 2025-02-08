from typing import List, Optional, TypeVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from src.shared.abstract.abstract_repository import AbstractRepository

T = TypeVar('T')
G = TypeVar('G')

class PostgresRepository(AbstractRepository[T]):
    def __init__(self, connection_url: str, model: G):
        self.model: G = model
        self.connection_url = connection_url
        self.engine = create_async_engine(self.connection_url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def insert(self, data: dict) -> T | None:
        async with self.SessionLocal() as session:
            async with session.begin():
                entity: G = self.model(**data)
                session.add(entity)
                await session.flush()
                await session.refresh(entity)
                return entity
        return None

    async def find(self, data: dict) -> Optional[T]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(self.model).filter_by(**data))
            return result.scalars().first()

    async def find_all(self) -> List[T]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()
        return None

    async def update(self, id: int, data: dict) -> T:
        async with self.SessionLocal() as session:
            async with session.begin():
                entity = await self.find({"id": id})
                if entity:
                    for key, value in data.items():
                        setattr(entity, key, value)
                await session.commit()
                await session.refresh(entity)
                return entity

    async def delete(self, id: int) -> bool:
        async with self.SessionLocal() as session:
            async with session.begin():
                entity = await self.find({"id": id})
                print(entity)
                if not entity:
                    return False
                
                await session.delete(entity)
                await session.commit()
                return True

    async def execute(self, query: str) -> List[T] | T:
        async with self.SessionLocal() as session:
            async with session.begin():
                await session.execute(query)
