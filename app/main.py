from fastapi import FastAPI

from app.core.database import engine, Base
from app.api.routes.cargo import router as cargo_router
from app.api.routes.colaborador import router as colaborador_router


app = FastAPI(title="API de gerenciamento de colaboradores", version="1.0.0")

app.include_router(cargo_router, prefix="/cargos", tags=["cargos"])
app.include_router(colaborador_router, prefix="/colaboradores", tags=["colaboradores"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
