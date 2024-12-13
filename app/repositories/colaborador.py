from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.colaborador import Colaborador
from app.schemas.colaborador import ColaboradorCreate, ColaboradorUpdate
from sqlalchemy.orm import selectinload
from app.core.utils.errors import MensagensErro
from fastapi import HTTPException


class ColaboradorRepository:
    """
    Gerencia operações de CRUD de colaborades no banco.
    """

    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, colaborador_data):
        """
        Cria um novo colaborador
        """
        try:
            novo_colaborador = Colaborador(**colaborador_data.dict())
            self.database.add(novo_colaborador)
            await self.database.commit()
            await self.database.refresh(novo_colaborador)

            query = (
                select(Colaborador)
                .options(selectinload(Colaborador.cargo))
                .where(Colaborador.id == novo_colaborador.id)
            )
            result = await self.database.execute(query)
            return result.scalar_one()
        except IntegrityError:
            await self.database.rollback()
            raise HTTPException(
                status_code=400,
                detail=MensagensErro.ERRO_INTEGRIDADE,
            )
        except SQLAlchemyError as e:
            await self.database.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"{MensagensErro.ERRO_BANCO_DADOS}: {str(e)}",
            )

    async def list(self) -> list[Colaborador]:
        """
        Lista todos os colaboradores ativos
        """
        result = await self.database.execute(
            select(Colaborador).filter(Colaborador.status_colaborador == True)
        )
        return result.scalars().all()

    async def get_by_id(self, colaborador_id: str) -> Colaborador | None:
        """
        Retorna um colaborador buscando por id
        """
        result = await self.database.execute(
            select(Colaborador).filter(Colaborador.id == colaborador_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, colaborador_id: str, data: ColaboradorUpdate
    ) -> Colaborador | None:
        """
        Atualiza dados de um colaborador
        """
        colaborador = await self.database.get(Colaborador, colaborador_id)
        if not colaborador or not colaborador.status_colaborador:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(colaborador, key, value)
        await self.database.commit()
        await self.database.refresh(colaborador)
        return colaborador

    async def delete(self, colaborador_id: str) -> bool:
        """
        Deleta logicamente um colaborador
        """
        colaborador = await self.database.get(Colaborador, colaborador_id)
        if not colaborador or not colaborador.status_colaborador:
            return False
        colaborador.status_colaborador = False
        await self.database.commit()
        return True
