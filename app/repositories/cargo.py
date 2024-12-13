from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Cargo
from app.schemas import CargoCreate


class CargoRepository:
    """
    Gerencia CRUD de cargos.
    """

    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, cargo: CargoCreate):
        novo_cargo = Cargo(**cargo.dict())

        self.database.add(novo_cargo)
        await self.database.commit()
        await self.database.refresh(novo_cargo)

        return novo_cargo

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
