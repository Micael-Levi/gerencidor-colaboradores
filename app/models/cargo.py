from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False, unique=True)
    codigo = Column(String, nullable=False, unique=True)
    ativo = Column(Boolean, default=True)

    colaboradores = relationship(
        "Colaborador",
        back_populates="cargo",
        cascade="all, delete",
    )
