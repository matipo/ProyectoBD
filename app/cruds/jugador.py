from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Jugador

def create_jugador(session: Session, nombre: str, email: str, telefono: str, ciudad: str, fecha_inscripcion: Optional[datetime] = None):
    if fecha_inscripcion is None:
        fecha_inscripcion = datetime.now()
    jugador = Jugador(
        nombre=nombre,
        email=email,
        telefono=telefono,
        ciudad=ciudad,
        fecha_inscripcion=fecha_inscripcion
    )
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador

def get_jugador(session: Session, id: int):
    return session.query(Jugador).filter(Jugador.id == id).first()

def get_jugadores(session: Session):
    return session.query(Jugador).all()

def update_jugador(session: Session, id: int, nombre: str, email: str, telefono: str, ciudad: str):
    jugador = session.query(Jugador).filter(Jugador.id == id).first()
    if jugador is None:
        return None
    jugador.nombre = nombre
    jugador.email = email
    jugador.telefono = telefono
    jugador.ciudad = ciudad
    session.commit()
    session.refresh(jugador)
    return jugador

def delete_jugador(session: Session, id: int):
    jugador = session.query(Jugador).filter(Jugador.id == id).first()
    if jugador is None:
        return None
    session.delete(jugador)
    session.commit()
    return jugador
