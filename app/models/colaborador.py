from sqlalchemy import Column, String, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Colaborador(Base):
    __tablename__ = "colaborador"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    matricula = Column(String(50), unique=True, nullable=False)
    senha = Column(String(128), nullable=False)
    salario = Column(Float, nullable=False)
    status_colaborador = Column(Boolean, default=True)
    cargo_id = Column(UUID(as_uuid=True), ForeignKey("cargo.id"), nullable=False)
    cargo = relationship("Cargo", back_populates="colaboradores")
    lider_id = Column(UUID(as_uuid=True), ForeignKey("colaborador.id"), nullable=True)
    lider = relationship("Colaborador", remote_side=[id], backref="subordinados")
