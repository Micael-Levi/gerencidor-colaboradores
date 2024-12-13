import pytest
import uuid
from app.models.colaborador import Colaborador
from app.models.cargo import Cargo
from app.repositories.colaborador import ColaboradorRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


@pytest.mark.asyncio
async def test_criar_colaborador_sem_lider(database: AsyncSession):
    """Teste para criar um colaborador sem líder."""
    # Setup - Criar um cargo
    cargo = Cargo(
        id=uuid.uuid4(),
        nome="Gerente",
        codigo="MANAGER",
        ativo=True,
    )
    database.add(cargo)
    await database.commit()

    # Test - Criar um colaborador
    colaborador_repo = ColaboradorRepository(database)
    colaborador = Colaborador(
        id=uuid.uuid4(),
        nome="João",
        sobrenome="Silva",
        matricula="123456",
        senha="senhaSegura123",
        salario=5000.00,
        status_colaborador=True,
        cargo_id=cargo.id,
        lider_id=None,
    )
    database.add(colaborador)
    await database.commit()

    # Verificar no banco
    result = await database.execute(
        select(Colaborador).where(Colaborador.id == colaborador.id)
    )
    colaborador_db = result.scalar_one()
    assert colaborador_db.nome == "João"
    assert colaborador_db.cargo_id == cargo.id
    assert colaborador_db.lider_id is None


@pytest.mark.asyncio
async def test_criar_colaborador_com_lider(database: AsyncSession):
    """Teste para criar um colaborador com um líder."""
    # Setup - Criar um cargo
    cargo = Cargo(
        id=uuid.uuid4(),
        nome="Líder Técnico",
        codigo="LEAD",
        ativo=True,
    )
    database.add(cargo)
    await database.commit()

    # Criar o líder
    lider = Colaborador(
        id=uuid.uuid4(),
        nome="Carlos",
        sobrenome="Lima",
        matricula="987654",
        senha="senhaLider123",
        salario=8000.00,
        status_colaborador=True,
        cargo_id=cargo.id,
    )
    database.add(lider)
    await database.commit()

    # Test - Criar subordinado
    colaborador_repo = ColaboradorRepository(database)
    colaborador = Colaborador(
        id=uuid.uuid4(),
        nome="João",
        sobrenome="Silva",
        matricula="123457",
        senha="senhaSegura123",
        salario=5000.00,
        status_colaborador=True,
        cargo_id=cargo.id,
        lider_id=lider.id,
    )
    database.add(colaborador)
    await database.commit()

    # Verificar no banco
    result = await database.execute(
        select(Colaborador).where(Colaborador.id == colaborador.id)
    )
    colaborador_db = result.scalar_one()
    assert colaborador_db.nome == "João"
    assert colaborador_db.lider_id == lider.id


@pytest.mark.asyncio
async def test_atualizar_colaborador(database: AsyncSession):
    """Teste para atualizar informações de um colaborador."""
    # Setup - Criar um cargo e colaborador
    cargo = Cargo(
        id=uuid.uuid4(),
        nome="Desenvolvedor",
        codigo="DEV",
        ativo=True,
    )
    database.add(cargo)
    await database.commit()

    colaborador = Colaborador(
        id=uuid.uuid4(),
        nome="Ana",
        sobrenome="Oliveira",
        matricula="123458",
        senha="senhaSegura123",
        salario=4000.00,
        status_colaborador=True,
        cargo_id=cargo.id,
    )
    database.add(colaborador)
    await database.commit()

    # Atualizar colaborador
    colaborador_repo = ColaboradorRepository(database)
    colaborador.nome = "Ana Clara"
    colaborador.salario = 4500.00
    await database.commit()

    # Verificar no banco
    result = await database.execute(
        select(Colaborador).where(Colaborador.id == colaborador.id)
    )
    colaborador_db = result.scalar_one()
    assert colaborador_db.nome == "Ana Clara"
    assert colaborador_db.salario == 4500.00


@pytest.mark.asyncio
async def test_excluir_colaborador(database: AsyncSession):
    """Teste para excluir logicamente um colaborador."""
    # Setup - Criar um cargo e colaborador
    cargo = Cargo(
        id=uuid.uuid4(),
        nome="Tester",
        codigo="QA",
        ativo=True,
    )
    database.add(cargo)
    await database.commit()

    colaborador = Colaborador(
        id=uuid.uuid4(),
        nome="Marcos",
        sobrenome="Sousa",
        matricula="123459",
        senha="senhaSegura123",
        salario=3000.00,
        status_colaborador=True,
        cargo_id=cargo.id,
    )
    database.add(colaborador)
    await database.commit()

    # Excluir colaborador
    colaborador.status_colaborador = False
    await database.commit()

    # Verificar no banco
    result = await database.execute(
        select(Colaborador).where(Colaborador.id == colaborador.id)
    )
    colaborador_db = result.scalar_one()
    assert colaborador_db.status_colaborador is False
