from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_database
from app.repositories.colaborador import ColaboradorRepository
from app.schemas.colaborador import (
    ColaboradorCreate,
    ColaboradorUpdate,
    ColaboradorRead,
    ColaboradorReadFull,
)
from app.core.database import SessionLocal

router = APIRouter()


@router.post(
    "/",
    response_model=ColaboradorRead,
    summary="Criar colaborador",
    description="Registra um novo colaborador",
)
async def criar_colaborador(
    colaborador: ColaboradorCreate, database: AsyncSession = Depends(get_database)
):
    repo = ColaboradorRepository(database)
    return ColaboradorRead.from_orm(await repo.create(colaborador))


@router.get(
    "/",
    response_model=list[ColaboradorRead],
    summary="Listar colaboradores",
    description="Retorna todos os colaboradores ativos",
)
async def listar_colaboradores(database: AsyncSession = Depends(get_database)):
    repo = ColaboradorRepository(database)
    return await repo.list()


@router.get(
    "/{colaborador_id}",
    response_model=ColaboradorReadFull,
    summary="Lista um colaborador",
    description="Retorna todos os dados de um colaborador",
)
async def buscar_colaborador(
    colaborador_id: str, database: AsyncSession = Depends(get_database)
):
    repo = ColaboradorRepository(database)
    colaborador = await repo.get_by_id(colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador


@router.patch(
    "/{colaborador_id}",
    response_model=ColaboradorRead,
    summary="Atualizar colaborador",
    description="Atualiza os dados de um colaborador",
)
async def atualizar_colaborador(
    colaborador_id: str,
    data: ColaboradorUpdate,
    database: AsyncSession = Depends(get_database),
):
    repo = ColaboradorRepository(database)
    colaborador = await repo.update(colaborador_id, data)
    if not colaborador:
        raise HTTPException(
            status_code=404, detail="Colaborador não encontrado ou inativo"
        )
    return colaborador


@router.delete(
    "/{colaborador_id}",
    summary="Deleta um colaborador",
    description="Deleta logicamente um colaborador",
)
async def excluir_colaborador(
    colaborador_id: str, database: AsyncSession = Depends(get_database)
):
    repo = ColaboradorRepository(database)
    sucesso = await repo.delete(colaborador_id)
    if not sucesso:
        raise HTTPException(
            status_code=404, detail="Colaborador não encontrado ou já excluído"
        )
    return {"message": f"Colaborador com ID {colaborador_id} foi excluído logicamente."}
