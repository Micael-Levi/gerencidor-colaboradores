import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import (
    Base,
    get_database,
)

# Configuração do banco de dados de teste
DATABASE_TEST_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_TEST_URL, future=True)
SessionTest = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    """
    Cria e remove o esquema do banco de dados antes e depois de cada teste.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def database(setup_database):
    """
    Fornece uma sessão de banco de dados para os testes.
    """
    async with SessionTest() as session:
        yield session
        await session.close()


@pytest.fixture(scope="function")
def client(database):
    """
    Fixture para fornecer um cliente de teste para as rotas FastAPI.
    Sobrescreve a dependência do banco de dados.
    """
    app.dependency_overrides[get_database] = lambda: database
    return TestClient(app)
