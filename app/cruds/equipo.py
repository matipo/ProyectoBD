from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models import Equipo, Categoria, Jugador

def crear_equipo(Session: Session, nombre_equipo: str, jugadores: int, jugadores2: int, categoria: int):
    if jugadores == jugadores2:
        raise ValueError("Los jugadores deben ser diferentes")

    if not jugadores or not jugadores2:
        raise ValueError("Debe ingresar dos jugadores")

    categoria_obj = Session.query(Categoria).filter(Categoria.id == categoria).first()
    if not categoria_obj:
        raise ValueError("La categoria no existe")

    jugador1_obj = Session.query(Jugador).filter(Jugador.id == jugadores).first()
    jugador2_obj = Session.query(Jugador).filter(Jugador.id == jugadores2).first()
    if not jugador1_obj or not jugador2_obj:
        raise ValueError("Uno o ambos jugadores no existen")

    equipo = Equipo(
        nombre_equipo=nombre_equipo,
        categoria=categoria_obj
    )

    equipo.jugadores = [jugador1_obj]
    equipo.jugadores2 = [jugador2_obj]

    
    Session.add(equipo)
    Session.commit()
    Session.refresh(equipo)
    return equipo

def obtener_equipos(Session: Session):
    return Session.query(Equipo).all()

def obtener_equipo(Session: Session, id: int):
    return Session.query(Equipo).filter(Equipo.id == id).first()

def obtener_equipos_categoria(Session: Session, categoria: int):
    return Session.query(Equipo).filter(Equipo.categoria == categoria).all()

def obtener_equipos_jugador(Session: Session, jugador: int):
    return Session.query(Equipo).filter(Equipo.jugadores == jugador or Equipo.jugadores2 == jugador).all()

def obtener_equipos_torneo(Session: Session, torneo: int):
    return Session.query(Equipo).filter(Equipo.torneo == torneo).all()

def obtener_equipos_asociacion(Session: Session, asociacion: int):
    return Session.query(Equipo).filter(Equipo.asociacion == asociacion).all()


def actualizar_equipo(
    session: Session,
    equipo: int,
    categoria: Optional[int] = None,
    nombre_equipo: Optional[str] = None,
    jugadores: Optional[int] = None,
    jugadores2: Optional[int] = None,
):
    equipo_obj = session.query(Equipo).filter(Equipo.id == equipo).first()
    if not equipo_obj:
        return None

    if nombre_equipo:
        equipo_obj.nombre_equipo = nombre_equipo 

    if categoria:
        categoria_obj = session.query(Categoria).filter(Categoria.id == categoria).first()
        if not categoria_obj:
            raise ValueError("Categoría no existe")
        equipo_obj.categoria = categoria_obj

    if jugadores:
        jugador1_obj = session.query(Jugador).filter(Jugador.id == jugadores).first()
        if not jugador1_obj:
            raise ValueError("Jugador 1 no existe")
        equipo_obj.jugadores = [jugador1_obj]  # o depende de cómo esté tu relación

    if jugadores2:
        jugador2_obj = session.query(Jugador).filter(Jugador.id == jugadores2).first()
        if not jugador2_obj:
            raise ValueError("Jugador 2 no existe")
        equipo_obj.jugadores2 = [jugador2_obj]

    try:
        session.commit()
        session.refresh(equipo_obj)
        return equipo_obj
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