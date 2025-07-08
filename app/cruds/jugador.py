from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Usuario


def create_participante(session: Session, nombre: str, email: str, telefono: str, ciudad: str, fecha_inscripcion: Optional[datetime] = None):
  if fecha_inscripcion is None:
    fecha_inscripcion = datetime.now()
  usuario = Usuario(nombre=nombre, email=email, fecha_inscripcion=fecha_inscripcion, telefono=telefono, ciudad=ciudad)
  session.add(usuario)
  session.commit()
  session.refresh(usuario)
  return usuario

def get_participante(session: Session, id: int):
  return session.query(Usuario).filter(Usuario.id == id).first()

def get_participantes(session: Session):
  return session.query(Usuario).all()

def actualizar_participante(session: Session, id: int, nombre: str, email: str, telefono: str, ciudad: str):
  usuario = session.query(Usuario).filter(Usuario.id == id).first()
  usuario.nombre = nombre
  usuario.email = email
  usuario.telefono = telefono
  usuario.ciudad = ciudad
  session.commit()
  session.refresh(usuario)
  return usuario

def eliminar_participante(session: Session, id: int):
  usuario = session.query(Usuario).filter(Usuario.id == id).first()
  session.delete(usuario)
  session.commit()
  return usuario