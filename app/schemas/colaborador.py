from pydantic import BaseModel, Field
from app.schemas import CargoRead
import uuid


class ColaboradorBase(BaseModel):
    nome: str = Field(..., max_length=100)
    sobrenome: str = Field(..., max_length=100)
    matricula: str = Field(..., max_length=50)
    cargo_id: str
    lider_id: str | None = None


class ColaboradorCreate(ColaboradorBase):
    senha: str = Field(..., min_length=8)
    salario: float = Field(..., gt=0)


class ColaboradorUpdate(BaseModel):
    nome: str | None = None
    sobrenome: str | None = None
    senha: str | None = None
    salario: float | None = None
    cargo_id: str | None = None
    lider_id: str | None = None
    status_colaborador: bool | None = None


class ColaboradorRead(BaseModel):
    id: uuid.UUID
    nome: str
    sobrenome: str
    matricula: str
    salario: float
    status_colaborador: bool
    cargo_id: uuid.UUID
    lider_id: uuid.UUID | None = None

    class Config:
        from_attributes = True


class ColaboradorRetrieve(ColaboradorRead):
    lider: ColaboradorRead | None = None
    cargo: CargoRead | None = None
