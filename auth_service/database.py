from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("AUTH_DB_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_db():
    await engine.dispose()


async def get_db():
    async with SessionLocal() as session:
        yield session