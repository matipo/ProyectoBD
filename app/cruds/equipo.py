from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models import Equipo, Categoria

def crear_equipo(Session: Session, nombre: str, jugador1: int, jugador2: int, categoria: int, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()

    if jugador1 == jugador2:
        raise ValueError("Los jugadores deben ser diferentes")

    if not jugador1 or not jugador2:
        raise ValueError("Debe ingresar dos jugadores")

    categoria_obj = Session.query(Categoria).filter(Categoria.id == categoria).first()
    if not categoria_obj:
        raise ValueError("La categoria no existe")

  
    equipo = Equipo(nombre=nombre, jugador1=jugador1, jugador2=jugador2, categoria=categoria_obj, fecha_creacion=fecha_creacion)
    try:
        Session.add(equipo)
        Session.commit()
        return equipo
    except IntegrityError:
        Session.rollback()
        raise ValueError("El equipo ya existe")

def obtener_equipos(Session: Session):
    return Session.query(Equipo).all()

def obtener_equipo(Session: Session, id: int):
    return Session.query(Equipo).filter(Equipo.id == id).first()

def obtener_equipos_categoria(Session: Session, categoria: int):
    return Session.query(Equipo).filter(Equipo.categoria == categoria).all()

def obtener_equipos_jugador(Session: Session, jugador: int):
    return Session.query(Equipo).filter(Equipo.jugador1 == jugador or Equipo.jugador2 == jugador).all()

def obtener_equipos_torneo(Session: Session, torneo: int):
    return Session.query(Equipo).filter(Equipo.torneo == torneo).all()

def obtener_equipos_asociacion(Session: Session, asociacion: int):
    return Session.query(Equipo).filter(Equipo.asociacion == asociacion).all()


def actualizar_equipo(
    session: Session,
    equipo: int,
    nombre: Optional[str] = None,
    jugador1: Optional[int] = None,
    jugador2: Optional[int] = None
):
  equipo = session.query(Equipo).filter(Equipo.id == equipo).first()
  if not equipo:
    return None

  if nombre:
    equipo.nombre = nombre 
  if jugador1:
    equipo.jugador1 = jugador1
  if jugador2:
    equipo.jugador2 = jugador2

  try:
    session.commit()
    return equipo
  except IntegrityError:
    session.rollback()
    raise ValueError("No se pudo actualizar el equipo")

def eliminar_equipo(Session: Session, id: int) -> bool:
    equipo = Session.query(Equipo).filter(Equipo.id == id).first()
    if equipo and not equipo.partidos and not equipo.inscripciones:
        Session.delete(equipo)
        Session.commit()
        return True
    return False