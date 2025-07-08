from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Equipo

def create_equipo(session: Session, *, nombre_equipo: str,
                  categoria_id: int) -> Equipo:
    e = Equipo(nombre_equipo=nombre_equipo, categorias=categoria_id)
    session.add(e); session.commit(); session.refresh(e); return e

def get_equipo(session: Session, equipo_id: int) -> Optional[Equipo]:
    return session.get(Equipo, equipo_id)

def get_equipos(session: Session) -> List[Equipo]:
    return session.query(Equipo).all()

def update_equipo(session: Session, equipo_id: int, *, nombre_equipo: str,
                  categoria_id: int) -> Optional[Equipo]:
    e = session.get(Equipo, equipo_id)
    if not e: return None
    e.nombre_equipo = nombre_equipo; e.categorias = categoria_id
    session.commit(); session.refresh(e); return e

def delete_equipo(session: Session, equipo_id: int) -> Optional[Equipo]:
    e = session.get(Equipo, equipo_id)
    if not e: return None
    session.delete(e); session.commit(); return e
