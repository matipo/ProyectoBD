from sqlalchemy.orm import Session
from ..models import Inscripcion
from typing import Optional

def crear_inscripcion(session: Session, categoria_id: int, torneo_id: int, jugador_id: Optional[int] = None, equipo_id: Optional[int] = None):
    inscripcion = Inscripcion(
        categorias=categoria_id,  
        torneos=torneo_id,
        jugador=jugador_id,
        equipo=equipo_id
    )
    session.add(inscripcion)
    session.commit()
    session.refresh(inscripcion)
    return inscripcion

def obtener_inscripcion(session: Session, id: int, categoria_id: int):
    return session.query(Inscripcion).filter(
        Inscripcion.id == id,
        Inscripcion.categorias == categoria_id
    ).first()

def obtener_inscripciones(session: Session):
    return session.query(Inscripcion).all()

def actualizar_inscripcion(session: Session, id: int, categoria_id: int,
                            jugador_id: Optional[int] = None, equipo_id: Optional[int] = None):
    inscripcion = session.query(Inscripcion).filter(
        Inscripcion.id == id,
        Inscripcion.categorias == categoria_id
    ).first()
    if not inscripcion:
        return None
    inscripcion.jugador = jugador_id
    inscripcion.equipo = equipo_id
    session.commit()
    session.refresh(inscripcion)
    return inscripcion

def eliminar_inscripcion(session: Session, id: int, categoria_id: int):
    inscripcion = session.query(Inscripcion).filter(
        Inscripcion.id == id,
        Inscripcion.categorias == categoria_id
    ).first()
    if not inscripcion:
        return None
    session.delete(inscripcion)
    session.commit()
    return inscripcion
