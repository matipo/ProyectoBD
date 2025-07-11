from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Jugador

def crear_jugador(session: Session, nombre: str,pais:str , telefono: str,genero: str, ciudad: str,fecha_nacimiento: datetime ,fecha_inscripcion: Optional[datetime] = None,asociaciones: Optional[int] = None):
    if fecha_inscripcion is None:
        fecha_inscripcion = datetime.now()

    
    jugador = Jugador(
        nombre=nombre,
        pais=pais,
        telefono=telefono,
        genero = genero,
        ciudad=ciudad,
        fecha_nacimiento = fecha_nacimiento,
        fecha_inscripcion=fecha_inscripcion,
        asociaciones=asociaciones
    )
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador

def obtener_jugador(session: Session, id: int):
    return session.query(Jugador).filter(Jugador.id == id).first()

def obtener_jugadores(session: Session):
    return session.query(Jugador).all()

def actualizar_jugador(session: Session, id: int, nombre: str, pais:str, telefono: str, ciudad: str, fecha_nacimiento:datetime):
    jugador = session.query(Jugador).filter(Jugador.id == id).first()
    if jugador is None:
        return None
    jugador.nombre = nombre
    jugador.pais = pais
    jugador.telefono = telefono
    jugador.ciudad = ciudad
    jugador.fecha_nacimiento = fecha_nacimiento
    session.commit()
    session.refresh(jugador)
    return jugador

def eliminar_jugador(session: Session, id: int):
    jugador = session.query(Jugador).filter(Jugador.id == id).first()
    if jugador is None:
        return None
    session.delete(jugador)
    session.commit()
    return jugador
