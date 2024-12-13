from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Cargo
from app.schemas import CargoCreate
from app.core.utils.errors import MensagensErro
from fastapi import HTTPException


class CargoRepository:
    """
    Gerencia CRUD de cargos.
    """

    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, cargo: CargoCreate | dict):
        """
        Cria um novo cargo.
        Aceita tanto objetos Pydantic quanto dicionários.
        """

        try:
            if isinstance(cargo, dict):
                novo_cargo = Cargo(**cargo)
            else:
                novo_cargo = Cargo(**cargo.dict())

            self.database.add(novo_cargo)
            await self.database.commit()
            await self.database.refresh(novo_cargo)

            return novo_cargo
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

    async def get_all(self):
        queryset = await self.database.execute(select(Cargo))
        return queryset.scalars().all()

    async def update(self, cargo_id: str, nome: str = None, codigo: str = None):
        queryset = await self.database.execute(
            select(Cargo).where(Cargo.id == cargo_id)
        )
        cargo = queryset.scalar_one_or_none()
        if not cargo:
            return None
        if nome:
            cargo.nome = nome
        if codigo:
            cargo.codigo = codigo
        await self.database.commit()
        await self.database.refresh(cargo)
        return cargo

    async def delete(self, cargo_id: str):
        queryset = await self.database.execute(
            select(Cargo).where(Cargo.id == cargo_id)
        )
        cargo = queryset.scalar_one_or_none()
        if not cargo:
            return None
        cargo.ativo = False
        await self.database.commit()
        return cargo
