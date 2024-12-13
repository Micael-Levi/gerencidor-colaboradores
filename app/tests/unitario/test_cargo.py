import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cargo import Cargo
from app.repositories.cargo import CargoRepository


@pytest.mark.asyncio
async def test_criar_cargo(setup_database, database: AsyncSession):
    """
    Teste criação de cargo.
    """
    repository = CargoRepository(database)
    novo_cargo = await repository.create({"nome": "Gerente", "codigo": "MANAGER"})
    assert novo_cargo.nome == "Gerente"
    assert novo_cargo.codigo == "MANAGER"


@pytest.mark.asyncio
async def test_excluir_cargo(setup_database, database: AsyncSession):
    """
    Teste exclusão lógica de cargo.
    """
    repository = CargoRepository(database)
    cargo = await repository.create({"nome": "Gerente", "codigo": "MANAGER"})
    assert cargo.ativo is True

    await repository.delete(cargo.id)
    cargo_inativo = await database.get(Cargo, cargo.id)
    assert cargo_inativo.ativo is False
