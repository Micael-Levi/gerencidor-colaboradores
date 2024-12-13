from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CargoCreate, CargoRead, CargoUpdate, MensagemSucesso
from app.repositories import CargoRepository
from app.core.database import get_database

router = APIRouter()


@router.get(
    "/",
    response_model=List[CargoRead],
    summary="Listar cargos",
    description="Retorna todos os cargos",
)
async def list_jobs(db: AsyncSession = Depends(get_database)):
    """
    Endpoint para listar todos os cargos.
    """
    repo = CargoRepository(db)
    return await repo.get_all()  # Adicione await aqui


@router.post(
    "/",
    response_model=CargoRead,
    summary="Criar cargo",
    description="Cria um novo cargo",
)
async def criar_cargo(
    cargo: CargoCreate, database: AsyncSession = Depends(get_database)
):
    repository = CargoRepository(database)
    return await repository.create(cargo)


@router.patch(
    "/{cargo_id}",
    response_model=CargoRead,
    summary="Atualizar cargo",
    description="Atualiza nome ou código de um cargo",
)
async def atualizar_cargo(
    cargo_id: str,
    cargo_update: CargoUpdate,
    database: AsyncSession = Depends(get_database),
):
    repository = CargoRepository(database)
    cargo = await repository.update(
        cargo_id=cargo_id,
        nome=cargo_update.nome,
        codigo=cargo_update.codigo,
    )

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")

    return cargo


@router.delete(
    "/{cargo_id}",
    response_model=MensagemSucesso,
    summary="Excluir cargo",
    description="Exclui cargo em nível logico",
)
async def excluir_cargo(cargo_id: str, database: AsyncSession = Depends(get_database)):
    repository = CargoRepository(database)
    cargo = await repository.delete(cargo_id)

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")

    return {"mensagem": f"Cargo com ID {cargo_id} foi excluído logicamente."}
