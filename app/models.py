from sqlalchemy import Column, Integer, String, ForeignKey, Time
from .db import Base


class Alumno(Base):
    __tablename__ = "alumno"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)


class Profesor(Base):
    __tablename__ = "profesor"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)


class Curso(Base):
    __tablename__ = "curso"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    profesor = Column(
        Integer, ForeignKey("profesor.id", ondelete="CASCADE"), nullable=False
    )


class AlumnoCurso(Base):
    __tablename__ = "alumno_curso"
    alumno = Column(Integer, ForeignKey("alumno.id"), primary_key=True)
    curso = Column(Integer, ForeignKey("curso.id"), primary_key=True)


class Sala(Base):
    __tablename__ = "sala"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)


class Horario(Base):
    __tablename__ = "horario"
    id = Column(Integer, primary_key=True)
    dia = Column(String, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    sala = Column(Integer, ForeignKey("sala.id", ondelete="CASCADE"), nullable=False)
    curso = Column(Integer, ForeignKey("curso.id", ondelete="CASCADE"), nullable=False)
