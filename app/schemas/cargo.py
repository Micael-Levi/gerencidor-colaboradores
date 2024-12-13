import uuid
from pydantic import BaseModel, Field


class CargoCreate(BaseModel):
    """
    Esquema para criação de cargos.
    """

    nome: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nome do cargo (mínimo 3 e máximo 50 caracteres)",
    )
    codigo: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Código único do cargo (mínimo 2 e máximo 10 caracteres)",
    )


class CargoRead(BaseModel):
    """
    Esquema para leitura de cargos.
    """

    id: uuid.UUID
    nome: str
    codigo: str
    ativo: bool

    class Config:
        from_attributes = True


class CargoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=50)
    codigo: str | None = Field(None, min_length=2, max_length=10)
