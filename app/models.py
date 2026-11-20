from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Editorial(Base):
    __tablename__ = "editoriales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    pais = Column(String, nullable=False)
    email = Column(String, nullable=False)

    libros = relationship("Libro", back_populates="editorial", cascade="all, delete-orphan")


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    autor = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    anio = Column(Integer, nullable=False)
    existencia = Column(Integer, default=0, nullable=False)
    editorial_id = Column(Integer, ForeignKey("editoriales.id"), nullable=False)

    editorial = relationship("Editorial", back_populates="libros")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nomuser = Column(String, unique=True, index=True, nullable=False)
    passwd = Column(String, nullable=False)
    nombrecompleto = Column(String, nullable=False)