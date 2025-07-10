from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Torneo
from .mesa import crear_mesa

def crear_torneo(session, nombre, fechas_inscripcion, fecha_competencia, mesas_disponibles,mesas: Optional[int]= None, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
        fecha_creacion = fecha_creacion
    torneo = Torneo(
    nombre=nombre,
    fechas_inscripcion=fechas_inscripcion,
    fecha_competencia=fecha_competencia,
    mesas_disponibles=mesas_disponibles,
    mesas=mesas
    )
    session.add(torneo)
    session.commit()
    session.refresh(torneo)
    if mesas_disponibles !=None:
        for i in range(mesas_disponibles):
            crear_mesa(session, i+1,4,torneo.id,datetime.now(),)
    else:
        print("No se ejecuto", mesas_disponibles, print(torneo.id))
    
    return torneo


def obtener_torneo(session, id):
    return session.query(Torneo).filter(Torneo.id == id).first()   

def obtener_torneos(session):
    return session.query(Torneo).all()

def actualizar_torneo(session, id, nombre, fechas_inscripcion, fecha_competencia, mesas_disponibles):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    torneo.nombre = nombre
    torneo.fechas_inscripcion = fechas_inscripcion
    torneo.fecha_competencia = fecha_competencia
    torneo.mesas_disponibles = mesas_disponibles
    session.commit()
    return torneo

def eliminar_torneo(session, id):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    session.delete(torneo)
    session.commit()
    return torneo