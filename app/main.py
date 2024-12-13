from fastapi import FastAPI

from app.core.database import engine, Base

app = FastAPI(title="API de gerenciamento de colaboradores", version="1.0.0")


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
