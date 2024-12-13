from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.colaborador import Colaborador
from app.schemas.colaborador import ColaboradorCreate, ColaboradorUpdate
from sqlalchemy.orm import selectinload


class ColaboradorRepository:
    def __init__(self, database: AsyncSession):
        self.database = database

    async def create(self, colaborador_data):
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

    async def list(self) -> list[Colaborador]:
        result = await self.database.execute(
            select(Colaborador).filter(Colaborador.status_colaborador == True)
        )
        return result.scalars().all()

    async def get_by_id(self, colaborador_id: str) -> Colaborador | None:
        result = await self.database.execute(
            select(Colaborador).filter(Colaborador.id == colaborador_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, colaborador_id: str, data: ColaboradorUpdate
    ) -> Colaborador | None:
        colaborador = await self.database.get(Colaborador, colaborador_id)
        if not colaborador or not colaborador.status_colaborador:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(colaborador, key, value)
        await self.database.commit()
        await self.database.refresh(colaborador)
        return colaborador

    async def delete(self, colaborador_id: str) -> bool:
        colaborador = await self.database.get(Colaborador, colaborador_id)
        if not colaborador or not colaborador.status_colaborador:
            return False
        colaborador.status_colaborador = False
        await self.database.commit()
        return True
