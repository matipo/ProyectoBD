from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Torneo

def crear_torneo(sesion, nombre, fechas_inscripcion, fecha_competencia, mesas, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
        fecha_creacion = fecha_creacion
    torneo = Torneo(
    nombre=nombre,
    fechas_inscripcion=fechas_inscripcion,
    fecha_competencia=fecha_competencia,
    mesas=mesas
    )
    sesion.add(torneo)
    sesion.commit()
    return torneo

def obtener_torneo(sesion, id):
    return sesion.query(Torneo).filter(Torneo.id == id).first()   

def obtener_torneos(sesion):
    return sesion.query(Torneo).all()

def actualizar_torneo(sesion, id, nombre, fechas_inscripcion, fecha_competencia, mesas):
    torneo = sesion.query(Torneo).filter(Torneo.id == id).first()
    torneo.nombre = nombre
    torneo.fechas_inscripcion = fechas_inscripcion
    torneo.fecha_competencia = fecha_competencia
    torneo.mesas = mesas
    sesion.commit()
    return torneo

def eliminar_torneo(sesion, id):
    torneo = sesion.query(Torneo).filter(Torneo.id == id).first()
    sesion.delete(torneo)
    sesion.commit()
    return torneo