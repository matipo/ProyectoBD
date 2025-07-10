from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Asociacion

def crear_asociacion(session: Session, nombre: str, ciudad: str, pais:str, fecha_inscripcion: Optional[datetime] = None):
    if fecha_inscripcion is None:
        fecha_inscripcion = datetime.now()
        
        asociacion = Asociacion(nombre=nombre, ciudad=ciudad, pais=pais, fecha_inscripcion=fecha_inscripcion)
        session.add(asociacion)
        session.commit()
        session.refresh(asociacion)
        return asociacion

def obtener_asociacion(session: Session, id: int):
    return session.query(Asociacion).filter(Asociacion.id == id).first()

def obtener_asociaciones(session: Session):
    return session.query(Asociacion).all()

def actualizar_asociacion(session: Session, id: int, nombre: str, ciudad: str,pais:str):
    asociacion = session.query(Asociacion).filter(Asociacion.id == id).first()
    asociacion.nombre = nombre
    asociacion.ciudad = ciudad
    asociacion.pais = pais
    session.commit()
    session.refresh(asociacion)
    return asociacion

def eliminar_asociacion(session: Session, id: int):
    asociacion = session.query(Asociacion).filter(Asociacion.id == id).first()
    session.delete(asociacion)
    session.commit()
    return asociacion
  