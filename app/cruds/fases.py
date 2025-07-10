from sqlalchemy.orm import Session
from ..models import Fase

def crear_fase(session: Session, tipo: str, nombre: str, torneo_id: int, partido_id: int):
    fase = Fase(
        tipo=tipo,
        nombre=nombre,
        torneos=torneo_id,
        partidos=partido_id
    )
    session.add(fase)
    session.commit()
    session.refresh(fase)
    return fase

def obtener_fase(session: Session, id: int):
    return session.query(Fase).filter(Fase.id == id).first()

def obtener_fases(session: Session):
    return session.query(Fase).all()

def actualizar_fase(session: Session, id: int, tipo: str, nombre: str, torneo_id: int, partido_id: int):
    fase = session.query(Fase).filter(Fase.id == id).first()
    if not fase:
        return None
    fase.tipo = tipo
    fase.nombre = nombre
    fase.torneos = torneo_id
    fase.partidos = partido_id
    session.commit()
    session.refresh(fase)
    return fase

def eliminar_fase(session: Session, id: int):
    fase = session.query(Fase).filter(Fase.id == id).first()
    if not fase:
        return None
    session.delete(fase)
    session.commit()
    return fase
