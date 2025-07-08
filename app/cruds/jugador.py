from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from app.models import Jugador

def create_jugador(session: Session, *, pais: str, fecha_nacimiento: date,
                   genero: str, ciudad: str,
                   asociacion_id: Optional[int] = None) -> Jugador:
    j = Jugador(pais=pais, fecha_nacimiento=fecha_nacimiento,
                genero=genero, ciudad=ciudad,
                asociaciones=asociacion_id)
    session.add(j); session.commit(); session.refresh(j); return j

def get_jugador(session: Session, jugador_id: int) -> Optional[Jugador]:
    return session.get(Jugador, jugador_id)

def get_jugadores(session: Session) -> List[Jugador]:
    return session.query(Jugador).all()

def update_jugador(session: Session, jugador_id: int, *, pais: str,
                   fecha_nacimiento: date, genero: str, ciudad: str,
                   asociacion_id: Optional[int] = None) -> Optional[Jugador]:
    j = session.get(Jugador, jugador_id); 
    if not j: return None
    j.pais = pais; j.fecha_nacimiento = fecha_nacimiento
    j.genero = genero; j.ciudad = ciudad; j.asociaciones = asociacion_id
    session.commit(); session.refresh(j); return j

def delete_jugador(session: Session, jugador_id: int) -> Optional[Jugador]:
    j = session.get(Jugador, jugador_id)
    if not j: return None
    session.delete(j); session.commit(); return j
