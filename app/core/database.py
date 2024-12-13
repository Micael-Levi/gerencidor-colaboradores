from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)
Base = declarative_base()


def get_database():
    """Gerencia instância banco de dados"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
