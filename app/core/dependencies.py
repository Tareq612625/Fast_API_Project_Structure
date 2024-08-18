from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models.base import Base  # Import Base from base.py
from app.services.user_service import UserService
from app.db.repositories.user_repository import UserRepository
from fastapi import Depends

# Directly specify the database URL here
DATABASE_URL = "mssql+aioodbc://aziz:admin123@localhost/fast_api_app?driver=ODBC+Driver+17+for+SQL+Server"

# Create the async engine with the database URL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory bound to the async engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        # Create all tables in the database that are defined by Base's subclasses
        await conn.run_sync(Base.metadata.create_all)

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)