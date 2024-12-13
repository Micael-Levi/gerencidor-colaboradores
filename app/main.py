from fastapi import FastAPI

from app.core.database import engine, Base
from app.api.routes.cargo import router as cargo_router

app = FastAPI(title="API de gerenciamento de colaboradores", version="1.0.0")

app.include_router(cargo_router, prefix="/cargos", tags=["cargos"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
