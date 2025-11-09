import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Get or create the database engine"""
    global engine
    if not engine:
        db_url = f"mysql+asyncmy://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
        engine = create_async_engine(db_url, echo=True)
    return engine


async def get_session() -> AsyncSession:
    """Dependency to get database session"""
    engine = get_engine()
    async with AsyncSession(engine) as session:
        yield session


async def create_db_and_tables():
    """Create all database tables defined in SQLModel"""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db_connection():
    """Close database connection and dispose engine"""
    global engine
    if engine:
        await engine.dispose()
        engine = None


SessionDep = Annotated[AsyncSession, Depends(get_session)]
